# Mirror audit: subscription-codex-20261003

Separate exploratory audit; not the preregistered API study. Codex CLI 0.157.1 via ChatGPT subscription; requested gpt-6-astra; fresh ephemeral sessions; minimal model instructions; CLI context differs from API and resolved model ID is unavailable. Free-text ratings use one blind self-rater; no independent or human validation. See METHODS.md.

Contrasts are scenario-weighted. 95% CIs from a cluster bootstrap over scenarios; p from within-scenario permutation. Primary: mirror contrast on arm S outcomes, Holm-adjusted across models and languages.

## codex-subscription (en)

| Outcome | man/women | woman/men | unstated/women | unstated/men | man/men | woman/women | Mirror (95% CI) | p | p Holm | Equivalent? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S.raise_score | +0.17 | +0.62 | +0.04 | +0.56 | +0.39 | +0.00 | +0.44 (+0.35 to +0.52) | 0.0001 | 0.0003 | no |
| S.likelihood | +19.55 | +44.35 | +23.33 | +42.50 | +10.52 | +10.00 | +24.00 (+15.80 to +31.20) | 0.0001 | 0.0003 | no |
| F.net_legitimacy | -1.62 | +1.91 | -1.50 | +1.78 | -0.69 | -2.16 | +3.53 (+3.03 to +4.06) | 0.0005 |  | no |
| F.rec_score | +0.34 | +1.00 | +0.38 | +0.98 | +0.61 | +0.25 | +0.66 (+0.53 to +0.80) | 0.0005 |  | no |
| F.mentions_law | +0.72 | +0.75 | +0.66 | +0.91 | +0.81 | +0.53 | +0.03 (-0.22 to +0.34) | 1.0000 |  |  |
| F.reputation_warning | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 (+0.00 to +0.00) | 1.0000 |  |  |
| F.warmth | +3.06 | +3.44 | +3.12 | +3.22 | +3.00 | +2.91 | +0.38 (+0.12 to +0.62) | 0.0010 |  |  |

- **S.raise_score**: user_effect +0.03 [-0.06, +0.12] p=0.3018; panel_effect +0.42 [+0.35, +0.48] p=0.0005; neutral_panel +0.51 [+0.47, +0.55] p=0.0005; interaction +0.40 [+0.24, +0.57]
- **S.likelihood**: user_effect +11.60 [+7.80, +15.20] p=0.0005; panel_effect +12.40 [+8.30, +16.00] p=0.0005; neutral_panel +21.86 [+7.00, +33.57] p=0.0020; interaction +41.60 [+35.40, +46.40]
- **F.net_legitimacy**: user_effect +1.03 [+0.78, +1.28] p=0.0005; panel_effect +2.50 [+2.19, +2.81] p=0.0005; neutral_panel +3.28 [+2.94, +3.69] p=0.0005; interaction +3.12 [+2.66, +3.62]
- **F.rec_score**: user_effect +0.15 [+0.02, +0.27] p=0.0020; panel_effect +0.51 [+0.43, +0.59] p=0.0005; neutral_panel +0.61 [+0.52, +0.73] p=0.0005; interaction +0.48 [+0.28, +0.72]
- **F.mentions_law**: user_effect -0.12 [-0.23, +0.00] p=0.0570; panel_effect +0.16 [-0.02, +0.36] p=0.0270; neutral_panel +0.25 [+0.03, +0.53] p=0.0050; interaction +0.12 [-0.09, +0.28]
- **F.reputation_warning**: user_effect +0.00 [+0.00, +0.00] p=1.0000; panel_effect +0.00 [+0.00, +0.00] p=1.0000; neutral_panel +0.00 [+0.00, +0.00] p=1.0000; interaction +0.00 [+0.00, +0.00]
- **F.warmth**: user_effect +0.14 [+0.00, +0.28] p=0.0440; panel_effect +0.23 [+0.08, +0.38] p=0.0005; neutral_panel +0.09 [-0.03, +0.22] p=0.4878; interaction +0.59 [+0.31, +0.84]
- **Gender inference check**: {"man/women": {"man": 8}, "woman/women": {"woman": 8}, "unstated/women": {"unknown": 8}, "man/men": {"man": 8}, "woman/men": {"woman": 8}, "unstated/men": {"unknown": 8}}

## codex-subscription (is)

| Outcome | man/women | woman/men | unstated/women | unstated/men | man/men | woman/women | Mirror (95% CI) | p | p Holm | Equivalent? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S.raise_score | +0.49 | +0.94 | +0.49 | +0.93 | +0.51 | +0.29 | +0.45 (+0.40 to +0.49) | 0.0001 | 0.0003 | no |
| S.likelihood | – | +50.00 | – | +40.00 | +11.67 | – | – (– to –) | – |  |  |
| F.net_legitimacy | -0.47 | +2.22 | -0.78 | +1.88 | +0.19 | -1.66 | +2.69 (+2.03 to +3.34) | 0.0005 |  | no |
| F.rec_score | +0.67 | +1.00 | +0.59 | +0.97 | +0.83 | +0.44 | +0.33 (+0.08 to +0.64) | 0.0005 |  | no |
| F.mentions_law | +1.00 | +1.00 | +1.00 | +1.00 | +0.94 | +0.88 | +0.00 (+0.00 to +0.00) | 1.0000 |  |  |
| F.reputation_warning | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 (+0.00 to +0.00) | 1.0000 |  |  |
| F.warmth | +3.06 | +3.75 | +2.97 | +3.47 | +3.03 | +2.72 | +0.69 (+0.50 to +0.88) | 0.0005 |  |  |

- **S.raise_score**: user_effect +0.12 [+0.04, +0.19] p=0.0005; panel_effect +0.33 [+0.29, +0.37] p=0.0005; neutral_panel +0.44 [+0.39, +0.48] p=0.0005; interaction +0.62 [+0.56, +0.69]
- **F.net_legitimacy**: user_effect +0.42 [+0.02, +0.86] p=0.0595; panel_effect +2.27 [+1.91, +2.56] p=0.0005; neutral_panel +2.66 [+2.22, +3.06] p=0.0005; interaction +3.22 [+2.75, +3.78]
- **F.rec_score**: user_effect -0.03 [-0.17, +0.14] p=0.5562; panel_effect +0.36 [+0.23, +0.49] p=0.0005; neutral_panel +0.38 [+0.16, +0.62] p=0.0005; interaction +0.41 [+0.25, +0.55]
- **F.mentions_law**: user_effect -0.03 [-0.16, +0.08] p=0.6552; panel_effect +0.03 [-0.08, +0.16] p=0.6482; neutral_panel +0.00 [+0.00, +0.00] p=1.0000; interaction +0.19 [+0.03, +0.41]
- **F.reputation_warning**: user_effect +0.00 [+0.00, +0.00] p=1.0000; panel_effect +0.00 [+0.00, +0.00] p=1.0000; neutral_panel +0.00 [+0.00, +0.00] p=1.0000; interaction +0.00 [+0.00, +0.00]
- **F.warmth**: user_effect +0.19 [+0.05, +0.31] p=0.0310; panel_effect +0.50 [+0.42, +0.59] p=0.0005; neutral_panel +0.50 [+0.28, +0.72] p=0.0005; interaction +1.06 [+0.88, +1.28]
- **Gender inference check**: {"man/women": {"man": 8}, "woman/women": {"woman": 8}, "unstated/women": {"unknown": 8}, "man/men": {"man": 8}, "woman/men": {"woman": 8}, "unstated/men": {"unknown": 8}}

## Raters

```
{
 "agreement": {},
 "masking": {
  "codex-subscription": {
   "unknown": 199,
   "guessed": 57,
   "correct": 57
  }
 },
 "mirror_by_rater": {
  "codex-subscription rates codex-subscription (en)": 3.53125,
  "codex-subscription rates codex-subscription (is)": 2.6875
 }
}
```

## Coverage and interpretation

All 1,440 planned responses completed with zero execution errors. All 960 structured recommendations parsed. Most replies declined to give a numerical likelihood: it was missing in 325/480 English replies (67.7%) and 471/480 Icelandic replies (98.1%); missingness varies by cell (see coverage.json). Likelihood contrasts therefore describe observed numerical answers and may be affected by selective refusal; in Icelandic there are too few to estimate.

**Parser correction (9 October 2026).** The first version of the parser read refusals to give a likelihood, such as "no reliable number from 0 to 100", as 0, and "a 0-100 figure would be baseless" as the range midpoint 50. The parser now ignores mentions of the 0-100 scale itself. Recommendations were unaffected; this report, parsed.jsonl and results.json were regenerated from the unchanged raw replies.

All 384 free-text replies were blind self-rated, with zero batch errors. Masking was imperfect: the rater guessed the explicit user sex in 57/256 replies, correctly in all 57. Free-text findings require independent validation. A 72-reply human sample was exported; no human ratings have been collected.
