"""Runs the plan against configured models. Resumable: finished runs are skipped."""
import csv
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .providers import ProviderError, call
from .util import read_json, slug, study_dir, write_json


def model_by_id(cfg, mid):
    for m in cfg["models"]:
        if m["id"] == mid:
            return m
    raise SystemExit(f"No model with id '{mid}' in config. Known: {[m['id'] for m in cfg['models']]}")


def select(plan, arms=None, langs=None, limit_scenarios=None):
    rows = [r for r in plan if (not arms or r["arm"] in arms) and (not langs or r["lang"] in langs)]
    if limit_scenarios:
        keep = sorted({r["scenario"] for r in rows})[:limit_scenarios]
        rows = [r for r in rows if r["scenario"] in keep]
    return rows


def run_model(cfg, mid, arms=None, langs=None, limit_scenarios=None, max_reps=None, log=print):
    m = model_by_id(cfg, mid)
    d = study_dir(cfg)
    plan = read_json(d / "plan.json")
    rows = select(plan, arms, langs, limit_scenarios)
    if max_reps:
        rows = [r for r in rows if r["rep"] <= max_reps]
    out = d / "raw" / slug(mid)
    out.mkdir(parents=True, exist_ok=True)
    todo = [r for r in rows if not (out / f"{r['plan_id']}.json").exists()]
    # Each model gets its own seeded execution order, so time-of-day effects do not line up with cells
    random.Random(f"{cfg['study']['seed']}-{mid}").shuffle(todo)
    log(f"[{mid}] {len(rows)} runs in selection, {len(todo)} to do")
    max_tokens = m.get("max_output_tokens", cfg["study"]["max_output_tokens"])

    def one(r):
        t0 = time.time()
        rec = {k: r[k] for k in ("plan_id", "lang", "scenario", "arm", "U", "P", "rep")}
        rec.update(model_id=mid, provider=m["provider"], model_requested=m.get("model"))
        try:
            res = call(m, r["system"], r["message"], max_tokens)
            rec.update(text=res["text"], model_reported=res["model_reported"], attempts=res["attempts"], error=None)
            raw = res["raw"]
        except ProviderError as e:
            rec.update(text=None, error=str(e))
            raw = None
        rec["seconds"] = round(time.time() - t0, 1)
        rec["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if rec["error"] is None:
            write_json(out / f"{r['plan_id']}.json", rec)
            if m.get("keep_raw", False):
                write_json(out / "_raw" / f"{r['plan_id']}.json", raw)
        else:
            write_json(out / "_errors" / f"{r['plan_id']}.json", rec)
        return rec

    done = errs = 0
    with ThreadPoolExecutor(max_workers=m.get("concurrency", cfg["study"]["concurrency"])) as ex:
        futs = [ex.submit(one, r) for r in todo]
        for f in as_completed(futs):
            rec = f.result()
            done += 1
            errs += rec["error"] is not None
            if done % 25 == 0 or done == len(todo):
                log(f"[{mid}] {done}/{len(todo)} done, {errs} errors")
    return done, errs


def export_manual(cfg, arms, langs, max_reps, path):
    """Writes prompts for running in a consumer app (e.g. ChatGPT or Gemini with memory off)."""
    plan = read_json(study_dir(cfg) / "plan.json")
    rows = [r for r in select(plan, arms, langs) if r["rep"] <= max_reps]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["plan_id", "lang", "arm", "message", "response"])
        for r in rows:
            w.writerow([r["plan_id"], r["lang"], r["arm"], r["message"], ""])
    return len(rows)


def import_manual(cfg, mid, path):
    d = study_dir(cfg)
    plan = {r["plan_id"]: r for r in read_json(d / "plan.json")}
    out = d / "raw" / slug(mid)
    n = 0
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not (row.get("response") or "").strip():
                continue
            r = plan[row["plan_id"]]
            rec = {k: r[k] for k in ("plan_id", "lang", "scenario", "arm", "U", "P", "rep")}
            rec.update(model_id=mid, provider="manual", model_requested=None, model_reported=None,
                       text=row["response"], error=None, attempts=1, seconds=None, finished_utc=None)
            write_json(out / f"{r['plan_id']}.json", rec)
            n += 1
    return n


def selftest(cfg, mids=None):
    results = {}
    for m in cfg["models"]:
        if mids and m["id"] not in mids:
            continue
        try:
            res = call(m, "You are a helpful assistant.", "Reply with the single word: ready", 64, retries=2)
            results[m["id"]] = f"ok ({res['model_reported']}): {res['text'].strip()[:40]}"
        except Exception as e:  # noqa: BLE001
            results[m["id"]] = f"FAILED: {e}"
    return results
