# Exploratory Antigravity subscription mirror audit

This is a separate exploratory audit authorized on 2026-10-03. It is not the preregistered API study, and its observations must not be pooled with the pilot or a future API study.

The frozen plan contains 1,440 prompts: eight fictional scenarios, English and Icelandic, six user/panel cells, 10 structured replies and four free-text replies per cell, plus one gender-inference check. The plan SHA-256 is `c8772a87385ac59b377c298abb6a885ecd5792f8a17aef3592fde9a2e5d50149`. All 16 mirror checks passed.

Generation uses Antigravity CLI (agy) 1.2.16, requesting `gemini-3.8-flash-high` (the active default model setting at setup). Each call starts a new ephemeral session in a clean temporary directory. The scenario's minimal system prompt is supplied via `GEMINI.md` in the temporary directory. Slash commands and skills are disabled (`--disable-slash-commands`). The stream-json event stream is inspected to ensure that no tools or denied actions were executed; any unexpected tool use is rejected. The CLI may still include standard system/platform context; this is not a direct API test. CLI event streams and raw turn data are saved alongside responses. The stream independently reports the resolved model id (`gemini-3.8-flash-high`).

The CLI does not enforce the API output-token cap. Sampling and reasoning use the CLI defaults. Execution is shuffled and resumable, with four concurrent calls. Connection checks are excluded from the data.

Free-text replies are masked, shuffled, and blind-rated in fresh sessions using the same requested model. This is exploratory self-rating with one rater, not the protocol's independent three-vendor rating or human validation. A human sample is exported separately; no human ratings are claimed until collected.

The existing pipeline computes scenario-weighted contrasts, cluster-bootstrap intervals, permutation tests, and Holm correction within this audit. These remain exploratory statistics. The mirror contrast is (woman/all-male panel) minus (man/all-female panel); positive values indicate greater support for the woman. Missing, failed, and unparseable responses must be reported with the final coverage counts.
