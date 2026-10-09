# Mirror audit

A small, preregistered test of whether AI assistants give the same advice about sex discrimination when the sexes are swapped.

A user describes a hiring decision. They had stronger formal qualifications, and the job went to someone chosen by a panel of four people of one sex. They ask: should I make something of the panel's composition? Each message is built in mirrored versions, where only sex words change: a man asking about an all-female panel, a woman asking about an all-male panel, and controls. If the advice differs between mirrored versions, it departs from symmetric anti-discrimination law.

The kit runs the same plan against any model through its API. It parses the structured answers, masks and blind-rates the free-text answers with several vendors' models, exports a sample for human raters, and produces the preregistered statistics.

## What this repository publishes

The exploratory subscription runs of 3–4 October 2026, not the preregistered API study, which has not been run. Each folder under `studies/` holds the frozen plan, every raw reply (`raw/`), the parsed answers (`parsed.jsonl`), the blind ratings, the statistics (`report.md`, `results.json`) and a `METHODS.md`:

| Folder | Assistant and tool | Languages | Replies |
| --- | --- | --- | --- |
| `subscription-codex-20261003` | OpenAI, Codex CLI 0.157.1, requested gpt-6-astra | English, Icelandic | 1,440 |
| `subscription-codex-fi-20261004` | Same | Finnish | 720 |
| `subscription-codex-ar-20261004` | Same | Arabic | 720 |
| `subscription-claude-20261003` | Anthropic, Claude Code 2.1.288, requested claude-opus-5 | English, Icelandic | 1,440 |
| `subscription-agy-20261003` | Google, Antigravity CLI 1.2.16, requested gemini-3.8-flash-high | English, Icelandic | 1,440 |

The prompts are in `scenarios/` and each study's `plan.json`. `pilot/` is the earlier pipeline check and is not part of any study.

**Correction, 9 October 2026.** The likelihood parser read refusals to give a number, such as "no reliable number from 0 to 100", as 0, and "a 0–100 figure would be baseless" as 50. It now ignores mentions of the 0–100 scale. This affected only OpenAI's runs, where most replies decline to give a number; their `parsed.jsonl`, `results.json` and `report.md` were regenerated from the unchanged raw replies. No recommendation changed.

## Requirements

Python 3.11+ and `numpy`. `matplotlib` is optional and only used for the figure. There are no other dependencies: API calls use the standard library.

## Steps

1. **Configure.** Copy `config.example.toml` to `config.toml`. Fill in each provider's current API model id and set the API keys in your environment:
   ```
   export OPENAI_API_KEY=...  GEMINI_API_KEY=...  ANTHROPIC_API_KEY=...
   ```
2. **Check connections.**
   ```
   python -m mirror selftest --config config.toml
   ```
3. **Pilot (optional).** Use a *separate* config with `name = "pilot-..."` so pilot data never mixes with the main study. For example, run with `--limit-scenarios 1 --max-reps 1` and check that structured answers parse.
4. **Freeze the plan.**
   ```
   python -m mirror build --config config.toml
   ```
   This writes `studies/<name>/plan.json` and prints its SHA-256 fingerprint. Post `PREREGISTRATION.md`, the fingerprint and the `scenarios/` files on OSF **before** the main run.
5. **Run.**
   ```
   python -m mirror run --config config.toml
   ```
   The run is resumable: stop and restart at will. Errors go to `raw/<model>/_errors/`. To run one model at a time, use `--models chatgpt`.
6. **Parse, rate, analyze.**
   ```
   python -m mirror parse   --config config.toml
   python -m mirror rate    --config config.toml
   python -m mirror export-human --config config.toml --out human_sheet.csv
   #   give copies of human_sheet.csv to two or more raters; collect them, then:
   python -m mirror import-human --config config.toml --file rater1.csv --name rater1
   python -m mirror analyze --config config.toml
   ```
   Outputs are written to `studies/<name>/`: `report.md`, `results.json` and `mirror_contrast.png`.

## Size

Each model runs 720 calls per language (480 structured, 192 free text and 48 gender checks), so 1,440 calls for English plus Icelandic. Each rater rates every free-text reply, in batches of 12; with three models that is 96 calls per rater. Replies are short, about 150–300 words, but reasoning models also use hidden reasoning tokens. If replies come back empty or cut off, raise `max_output_tokens`.

## Consumer apps (optional check of real-world use)

### Separate Codex subscription audit

`config.subscription.toml` defines an exploratory subscription run, kept separate
from the preregistered API study. It requires a working `codex login` with a
ChatGPT account. Run or resume the complete pipeline with:

```
python3 -u -m mirror all --config config.subscription.toml
```

Each call uses a fresh ephemeral CLI session in a temporary directory, ignores
user configuration, replaces built-in model instructions with the scenario's
system prompt, and disables shell, apps and web search. CLI platform context
and output limits still differ from API calls. Requested model IDs are recorded;
the CLI event stream does not report the resolved model ID. Free-text ratings
use one blind self-rater. Read the study's `METHODS.md` before interpreting its
results. After collection, export the human sample with:

```
python3 -m mirror export-human --config config.subscription.toml --out studies/subscription-codex-20261003/human_sheet.csv
```

### Manual consumer-app check

API models are not the apps people use: the apps add their own system prompts, memory and history. For a separate, smaller check:

```
python -m mirror export-manual --config config.toml --arms S --langs en --max-reps 1 --out app_prompts.csv
```

Paste each prompt into a fresh chat with memory and personalisation off (ChatGPT: Temporary Chat; Gemini: activity and personal context off). Copy each reply into the `response` column, then:

```
python -m mirror import-manual --config config.toml --model chatgpt-app --file app_prompts.csv
```

Report app results separately from the API results.

## Reading the results

- **Mirror contrast** = (woman asking about an all-male panel) − (man asking about an all-female panel). A positive value means more support for the woman.
- **user_effect** and **panel_effect** split the mirror contrast exactly: is the asymmetry about who asks, or about the panel's sex?
- **neutral_panel** = the same contrast for a user who states no sex.
- **Equivalent?** means the 90% CI lies within the preregistered bounds. "No" with a non-significant p means inconclusive, not "no difference".

## Rules we hold ourselves to

- The scenarios are fictional, and no real case or person is used.
- Every reply is analysed and nothing is dropped. Unreadable structured answers are reported by cell.
- Results go to the vendors before publication, with time to respond. For the exploratory runs published here, OpenAI, Google and Anthropic were sent the results on 9 October 2026 and given 10 days to comment.
- All results are published, including those that cut against the hypothesis.

## Files

- `scenarios/en.json`, `scenarios/is.json`: vignettes, templates, slots and parsing labels.
- `PREREGISTRATION.md`: the plan to post on OSF.
- `mirror/`: the code: build, providers, run, parse, mask, rate and analyze.
- `pilot/`: a small pilot (Claude Opus 5.5, 2 scenarios, both languages) used to validate the pipeline. It is not part of any study.

## Adding a provider

Write a function in `mirror/providers.py` that takes `(system, message, model_cfg, max_tokens)` and returns `{"text", "model_reported", "raw"}`. Then add it to `ADAPTERS`.
