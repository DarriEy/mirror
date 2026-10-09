# Exploratory Claude subscription mirror audit

This is a separate exploratory audit authorized on 2026-10-03, run as a direct
comparison to `subscription-codex-20261003` (Codex CLI / ChatGPT subscription)
and `subscription-agy-20261003` (Antigravity CLI / Gemini subscription). It is
not the preregistered API study, and its observations must not be pooled with
the pilot or a future API study.

The frozen plan contains 1,440 prompts: eight fictional scenarios, English and
Icelandic, six user/panel cells, 10 structured replies and four free-text
replies per cell, plus one gender-inference check. The plan SHA-256 is
`c8772a87385ac59b377c298abb6a885ecd5792f8a17aef3592fde9a2e5d50149` — identical
to the Codex and Antigravity subscription plans, so all three audits ran the
exact same 1,440 prompts. All 16 mirror checks passed.

Generation uses Claude Code CLI 2.1.288, authenticated with a Claude
subscription, requesting `claude-opus-5` (the account's current default model
at setup time, set immediately before this audit began). Each call runs
`claude -p --no-session-persistence --strict-mcp-config --setting-sources ""
--disable-slash-commands --tools "" --model claude-opus-5 --system-prompt
<scenario system prompt> --output-format json`, so each turn is a fresh,
non-persisted session with no tools, no MCP servers, no project/user settings
and no CLAUDE.md discovery (`cwd` was a throwaway scratch directory, not the
study repository). The CLI's JSON result is used directly; usage metadata is
kept but the CLI does not report a separate "resolved model" distinct from
the requested id, so `model_reported` echoes the model actually billed for
the call. The CLI does not enforce the API output-token cap; sampling and
reasoning use the CLI's defaults. Execution is shuffled and resumable, with
four concurrent calls (`concurrency = 4`). Connection checks (`selftest`) are
excluded from the data.

**Interruptions.** Collection hit the account's rolling usage-session cap
repeatedly: once during the initial pass (noticed late, after the run had
already spent hours retrying doomed calls against a stale cap instead of
stopping), and twice more during a scripted backfill that killed the run as
soon as a cap error appeared and slept until the CLI-reported reset time
(each window was almost exactly five hours: resets at 2:50am, 7:50am, 12:50pm,
5:50pm and 10:50pm Atlantic/Reykjavik on 2026-10-03/04) before resuming. The
rating pass hit the same cap once (5/32 batches) and was backfilled the same
way after its stated reset. Every affected plan_id was simply retried after
the window reset — no prompt, cell, or scenario was skipped or substituted —
so the final data contain no gaps attributable to the cap; see
`coverage.json`. The practical effect is that this audit's wall-clock
collection time (roughly a day, spread over five usage windows) is not
comparable to Codex's or Antigravity's single-pass collection time, and the
45 calls that failed outright before being retried do not appear in the raw
error logs in their first, capped form (those transient records were
superseded by the successful retry written to the same `plan_id.json`).

Free-text replies are masked, shuffled, and blind-rated in fresh sessions
using the same requested model (`claude-opus-5`). This is exploratory
self-rating with one rater, not the protocol's independent three-vendor
rating or human validation. A human sample (72 rows, 20% stratified by
model/language/cell) is exported separately to `human_sheet.csv`; no human
ratings are claimed until collected.

The existing pipeline computes scenario-weighted contrasts, cluster-bootstrap
intervals, permutation tests, and Holm correction within this audit. These
remain exploratory statistics. The mirror contrast is (woman/all-male panel)
minus (man/all-female panel); positive values indicate greater support for
the woman. All 1,440 planned responses completed with zero execution errors
in the final data; all 960 structured replies parsed with zero missing
recommendation or likelihood values (see `coverage.json`). All 384 free-text
replies were blind self-rated with zero batch errors in the final data.
