# Exploratory Codex subscription mirror audit

This is a separate exploratory audit authorized on 2026-10-03. It is not the preregistered API study, and its observations must not be pooled with the pilot or a future API study.

The frozen plan contains 1,440 prompts: eight fictional scenarios, English and Icelandic, six user/panel cells, 10 structured replies and four free-text replies per cell, plus one gender-inference check. The plan SHA-256 is `c8772a87385ac59b377c298abb6a885ecd5792f8a17aef3592fde9a2e5d50149`. All 16 mirror checks passed.

Generation uses Codex CLI 0.157.1, authenticated with ChatGPT, requesting `gpt-6-astra` (the working CLI default at setup). Each call starts a new ephemeral session in a temporary directory. User configuration and execution rules are ignored; project instructions are disabled. The scenario's minimal system prompt replaces built-in model instructions through `model_instructions_file`. Shell tools, shell snapshots, apps, multi-agent features and web search are disabled. Unexpected tool activity is rejected. The CLI may still add platform context; this is not a direct API or consumer ChatGPT app test. CLI event streams are saved alongside raw responses. The stream does not independently report the resolved model id, so `model_reported` is null rather than an invented identifier.

The CLI does not enforce the API output-token cap. Sampling and reasoning use the CLI defaults. Execution is shuffled and resumable, with four concurrent calls. Connection checks are excluded from the data. Setup rejected `gpt-6.1-sol`; no scenario data were collected with that model.

Free-text replies are masked, shuffled, and blind-rated in fresh sessions using the same requested model. This is exploratory self-rating with one rater, not the protocol's independent three-vendor rating or human validation. A human sample is exported separately; no human ratings are claimed until collected.

The existing pipeline computes scenario-weighted contrasts, cluster-bootstrap intervals, permutation tests, and Holm correction within this audit. These remain exploratory statistics. The mirror contrast is (woman/all-male panel) minus (man/all-female panel); positive values indicate greater support for the woman. Missing, failed, and unparseable responses must be reported with the final coverage counts.
