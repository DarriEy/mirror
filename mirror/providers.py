"""Model adapters. Each takes (system, message, cfg) and returns a dict with
text, the model id reported by the provider, and the raw response.

Uses only the Python standard library (urllib). If a provider changes its API,
edit the matching function below; each is a few lines.
"""
import json
import os
import re
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.request

from .util import api_key


class ProviderError(Exception):
    def __init__(self, msg, retryable=False):
        super().__init__(msg)
        self.retryable = retryable


def _post(url, headers, body, timeout=300):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        raise ProviderError(f"HTTP {e.code}: {detail}", retryable=e.code in (408, 409, 429, 500, 502, 503, 504, 529))
    except (urllib.error.URLError, TimeoutError) as e:
        raise ProviderError(f"network: {e}", retryable=True)


def openai(system, message, m, max_tokens):
    body = {"model": m["model"], "messages": [{"role": "system", "content": system}, {"role": "user", "content": message}],
            "max_completion_tokens": max_tokens}
    body.update(m.get("extra", {}))
    base = m.get("base_url", "https://api.openai.com/v1")
    d = _post(f"{base}/chat/completions", {"Authorization": f"Bearer {api_key(m)}"}, body)
    text = d["choices"][0]["message"].get("content") or ""
    return {"text": text, "model_reported": d.get("model"), "raw": d}


def anthropic(system, message, m, max_tokens):
    body = {"model": m["model"], "max_tokens": max_tokens, "system": system,
            "messages": [{"role": "user", "content": message}]}
    body.update(m.get("extra", {}))
    d = _post("https://api.anthropic.com/v1/messages",
              {"x-api-key": api_key(m), "anthropic-version": "2023-06-01"}, body)
    text = "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
    return {"text": text, "model_reported": d.get("model"), "raw": d}


def gemini(system, message, m, max_tokens):
    body = {"systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": message}]}],
            "generationConfig": {"maxOutputTokens": max_tokens}}
    body.update(m.get("extra", {}))
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m['model']}:generateContent"
    d = _post(url, {"x-goog-api-key": api_key(m)}, body)
    cands = d.get("candidates") or []
    parts = (cands[0].get("content") or {}).get("parts", []) if cands else []
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    return {"text": text, "model_reported": d.get("modelVersion"), "raw": d}


def claude_cli(system, message, m, max_tokens):
    """Runs Claude through the Claude Code CLI with no tools, MCP servers,
    settings or session persistence (used for pilots inside Claude Code)."""
    cmd = ["claude", "-p", "--no-session-persistence", "--strict-mcp-config", "--setting-sources", "",
           "--disable-slash-commands", "--tools", "", "--model", m["model"], "--system-prompt", system,
           "--output-format", "json"]
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_POST_TURN_MEMORY", "CLAUDE_CODE_POST_TURN_MEMORY_CONFIG")}
    p = subprocess.run(cmd, input=message, capture_output=True, text=True, env=env, timeout=600,
                       cwd=m.get("cwd") or os.getcwd())
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise ProviderError(f"cli: {p.stderr[-300:] or p.stdout[-300:]}", retryable=True)
    if d.get("is_error"):
        raise ProviderError(f"cli error: {d.get('result')}", retryable=True)
    return {"text": d.get("result") or "", "model_reported": ",".join((d.get("modelUsage") or {}).keys()), "raw": {"usage": d.get("usage")}}


def codex_cli(system, message, m, max_tokens):
    """Fresh subscription-backed CLI turn; never shares the study directory.

    CLI context and output limits differ from the API adapters. Keep these
    responses in a separately labelled exploratory study.
    """
    with tempfile.TemporaryDirectory(prefix="mirror-codex-") as cwd:
        instructions = os.path.join(cwd, "instructions.txt")
        with open(instructions, "w", encoding="utf-8") as f:
            f.write(system)
        cmd = ["codex", "exec", "--ignore-user-config", "--ignore-rules",
               "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only",
               "--json", "-m", m["model"],
               "-c", "model_instructions_file=" + json.dumps(instructions),
               "-c", 'web_search="disabled"', "-c", "features.shell_tool=false",
               "-c", "features.shell_snapshot=false", "-c", "features.apps=false",
               "-c", "features.multi_agent=false", "-c", "project_doc_max_bytes=0",
               "-c", 'forced_login_method="chatgpt"', "-"]
        try:
            p = subprocess.run(cmd, input=message, capture_output=True, text=True,
                               cwd=cwd, timeout=m.get("timeout", 600))
        except subprocess.TimeoutExpired:
            raise ProviderError("codex CLI timed out", retryable=True)
        events = []
        for line in p.stdout.splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        failures = [e for e in events if e.get("type") in ("error", "turn.failed")]
        completed = any(e.get("type") == "turn.completed" for e in events)
        if p.returncode or failures or not completed:
            detail = json.dumps(failures)[-1000:] if failures else p.stderr[-1000:]
            raise ProviderError(f"codex CLI: {detail}", retryable=False)
        items = [e["item"] for e in events if e.get("type") == "item.completed"]
        # Reject unexpected tool activity rather than silently accepting a
        # response produced with additional information.
        if any(i.get("type") not in ("agent_message", "reasoning") for i in items):
            raise ProviderError("codex CLI used an unexpected tool")
        reply = "\n".join(i.get("text", "") for i in items if i.get("type") == "agent_message")
        return {"text": reply, "model_reported": None,
                "raw": {"events": events, "model_requested": m["model"],
                        "note": "CLI event stream does not report resolved model id; output token cap unsupported"}}


_quota_lock = threading.Lock()
_quota_until = 0


def _parse_reset_seconds(text):
    m = re.search(r"Resets in (?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", text)
    if m:
        h = int(m.group(1) or 0)
        mins = int(m.group(2) or 0)
        s = int(m.group(3) or 0)
        total = h * 3600 + mins * 60 + s
        if total > 0:
            return total
    return 180


def agy_cli(system, message, m, max_tokens):
    """Fresh subscription-backed CLI turn via Antigravity CLI (agy); never shares the study directory.

    CLI context and output limits differ from the API adapters. Keep these
    responses in a separately labelled exploratory study.
    """
    global _quota_until
    with _quota_lock:
        wait = _quota_until - time.time()
    if wait > 0:
        time.sleep(wait)

    with tempfile.TemporaryDirectory(prefix="mirror-agy-") as cwd:
        instructions = system + "\n\nDo not use any tools, commands, or web search. Provide your response directly as text."
        with open(os.path.join(cwd, "GEMINI.md"), "w", encoding="utf-8") as f:
            f.write(instructions)
        cmd = ["agy", "--disable-slash-commands", "--output-format", "stream-json"]
        if m.get("model"):
            cmd.extend(["--model", m["model"]])
        if m.get("effort"):
            cmd.extend(["--effort", m["effort"]])
        cmd.extend(["--print", message])
        try:
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                               timeout=m.get("timeout", 600))
        except subprocess.TimeoutExpired:
            raise ProviderError("agy CLI timed out", retryable=True)
        events = []
        for line in p.stdout.splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        init_evt = next((e for e in events if e.get("event") == "init"), {})
        result_evt = next((e for e in events if e.get("event") == "result"), {})
        result_data = result_evt.get("result", {})
        text = result_data.get("response", "")
        if p.returncode or result_data.get("status") != "SUCCESS":
            detail = p.stderr[-1000:] if p.stderr else text[-1000:]
            if any(k in detail for k in ("RESOURCE_EXHAUSTED", "quota reached", "code 429")):
                wait_sec = _parse_reset_seconds(detail) + 30
                with _quota_lock:
                    if time.time() + wait_sec > _quota_until:
                        _quota_until = time.time() + wait_sec
                        print(f"\n[agy quota] Rate limit hit. Pausing {wait_sec}s ({round(wait_sec/60, 1)}m) until quota resets...", flush=True)
                time.sleep(wait_sec)
                raise ProviderError(f"agy CLI: {detail}", retryable=True)
            raise ProviderError(f"agy CLI: {detail}", retryable=False)
        tool_steps = [e for e in events if e.get("event") == "step_update" and e.get("step_update", {}).get("step_type") not in ("user_input", "agent_response")]
        if tool_steps or result_data.get("denied_actions"):
            raise ProviderError("agy CLI used an unexpected tool", retryable=False)
        return {
            "text": text,
            "model_reported": init_evt.get("init", {}).get("model"),
            "raw": {
                "events": events,
                "model_requested": m.get("model"),
                "conversation_id": result_data.get("conversation_id"),
                "usage": result_data.get("usage"),
                "duration_seconds": result_data.get("duration_seconds"),
            }
        }


ADAPTERS = {"openai": openai, "anthropic": anthropic, "gemini": gemini, "claude_cli": claude_cli,
            "codex_cli": codex_cli, "agy_cli": agy_cli}


def call(model_cfg, system, message, max_tokens, retries=None):
    if retries is None:
        retries = model_cfg.get("retries", 15)
    fn = ADAPTERS[model_cfg["provider"]]
    delay = 5
    for attempt in range(1, retries + 1):
        try:
            out = fn(system, message, model_cfg, max_tokens)
            if not out["text"].strip():
                raise ProviderError("empty response", retryable=True)
            out["attempts"] = attempt
            return out
        except ProviderError as e:
            if not e.retryable or attempt == retries:
                raise
            time.sleep(delay)
            delay = min(delay * 2, 120)
