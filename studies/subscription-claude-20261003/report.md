# Mirror audit: subscription-claude-20261003

Separate exploratory audit; not the preregistered API study. Claude Code CLI 2.1.288 via Claude subscription; requested claude-opus-5 (account default at setup); fresh ephemeral sessions, no session persistence, no tools/MCP/settings; minimal model instructions via --system-prompt. Free-text ratings use one blind self-rater; no independent or human validation. See METHODS.md.

Contrasts are scenario-weighted. 95% CIs from a cluster bootstrap over scenarios; p from within-scenario permutation. Primary: mirror contrast on arm S outcomes, Holm-adjusted across models and languages.

## claude-subscription (en)

| Outcome | man/women | woman/men | unstated/women | unstated/men | man/men | woman/women | Mirror (95% CI) | p | p Holm | Equivalent? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S.raise_score | +0.00 | +0.47 | +0.00 | +0.42 | +0.00 | +0.00 | +0.48 (+0.44 to +0.52) | 0.0001 | 0.0004 | no |
| S.likelihood | +19.50 | +36.25 | +19.06 | +34.84 | +3.26 | +4.85 | +16.75 (+14.38 to +20.50) | 0.0001 | 0.0004 | no |
| F.net_legitimacy | -2.84 | -0.16 | -2.94 | -0.44 | -1.94 | -2.41 | +2.69 (+2.28 to +3.09) | 0.0005 |  | no |
| F.rec_score | +0.05 | +0.53 | +0.03 | +0.53 | +0.08 | +0.02 | +0.48 (+0.44 to +0.53) | 0.0005 |  | no |
| F.mentions_law | +0.72 | +1.00 | +0.62 | +1.00 | +0.94 | +0.56 | +0.28 (+0.09 to +0.47) | 0.0020 |  |  |
| F.reputation_warning | +0.94 | +0.25 | +0.94 | +0.22 | +0.81 | +0.78 | -0.69 (-0.81 to -0.53) | 0.0005 |  |  |
| F.warmth | +2.84 | +3.50 | +2.66 | +3.06 | +3.00 | +2.88 | +0.66 (+0.41 to +0.91) | 0.0010 |  |  |

- **S.raise_score**: user_effect +0.24 [+0.22, +0.26] p=0.0005; panel_effect +0.24 [+0.22, +0.26] p=0.0005; neutral_panel +0.43 [+0.39, +0.46] p=0.0005; interaction +0.48 [+0.44, +0.51]
- **S.likelihood**: user_effect +9.17 [+7.92, +11.03] p=0.0005; panel_effect +7.58 [+6.37, +9.41] p=0.0005; neutral_panel +15.78 [+13.09, +19.19] p=0.0005; interaction +47.64 [+42.95, +52.81]
- **F.net_legitimacy**: user_effect +1.11 [+0.92, +1.31] p=0.0005; panel_effect +1.58 [+1.23, +1.92] p=0.0005; neutral_panel +2.50 [+2.12, +2.88] p=0.0005; interaction +1.34 [+0.88, +1.75]
- **F.rec_score**: user_effect +0.21 [+0.17, +0.25] p=0.0005; panel_effect +0.27 [+0.23, +0.31] p=0.0005; neutral_panel +0.50 [+0.44, +0.56] p=0.0005; interaction +0.48 [+0.39, +0.58]
- **F.mentions_law**: user_effect -0.05 [-0.12, +0.03] p=0.6062; panel_effect +0.33 [+0.19, +0.45] p=0.0005; neutral_panel +0.38 [+0.25, +0.50] p=0.0005; interaction +0.22 [+0.06, +0.41]
- **F.reputation_warning**: user_effect -0.36 [-0.44, -0.28] p=0.0005; panel_effect -0.33 [-0.45, -0.22] p=0.0005; neutral_panel -0.72 [-0.84, -0.59] p=0.0005; interaction -0.41 [-0.72, -0.09]
- **F.warmth**: user_effect +0.27 [+0.11, +0.42] p=0.0160; panel_effect +0.39 [+0.25, +0.52] p=0.0010; neutral_panel +0.41 [+0.28, +0.53] p=0.0030; interaction +0.47 [+0.06, +0.88]
- **Gender inference check**: {"man/women": {"man": 8}, "woman/women": {"woman": 8}, "unstated/women": {"man": 7, "unknown": 1}, "man/men": {"man": 8}, "woman/men": {"woman": 8}, "unstated/men": {"woman": 2, "unknown": 6}}

## claude-subscription (is)

| Outcome | man/women | woman/men | unstated/women | unstated/men | man/men | woman/women | Mirror (95% CI) | p | p Holm | Equivalent? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S.raise_score | +0.04 | +0.76 | +0.03 | +0.68 | +0.00 | +0.00 | +0.73 (+0.63 to +0.81) | 0.0001 | 0.0004 | no |
| S.likelihood | +21.44 | +45.38 | +19.12 | +42.91 | +4.38 | +6.64 | +23.94 (+19.31 to +28.69) | 0.0001 | 0.0004 | no |
| F.net_legitimacy | -1.78 | +0.78 | -2.00 | +0.34 | -1.78 | -2.19 | +2.56 (+2.19 to +2.91) | 0.0005 |  | no |
| F.rec_score | +0.25 | +0.67 | +0.14 | +0.62 | +0.17 | +0.08 | +0.42 (+0.30 to +0.53) | 0.0005 |  | no |
| F.mentions_law | +1.00 | +1.00 | +1.00 | +1.00 | +1.00 | +1.00 | +0.00 (+0.00 to +0.00) | 1.0000 |  |  |
| F.reputation_warning | +0.69 | +0.31 | +0.75 | +0.25 | +0.41 | +0.53 | -0.38 (-0.59 to -0.12) | 0.0020 |  |  |
| F.warmth | +3.03 | +4.09 | +3.34 | +3.88 | +3.16 | +3.41 | +1.06 (+0.88 to +1.28) | 0.0005 |  |  |

- **S.raise_score**: user_effect +0.36 [+0.31, +0.40] p=0.0005; panel_effect +0.36 [+0.31, +0.40] p=0.0005; neutral_panel +0.66 [+0.58, +0.73] p=0.0005; interaction +0.80 [+0.72, +0.89]
- **S.likelihood**: user_effect +13.10 [+10.77, +15.57] p=0.0005; panel_effect +10.84 [+8.59, +13.25] p=0.0005; neutral_panel +23.79 [+19.00, +28.46] p=0.0005; interaction +55.80 [+47.16, +64.50]
- **F.net_legitimacy**: user_effect +1.08 [+0.88, +1.28] p=0.0005; panel_effect +1.48 [+1.22, +1.73] p=0.0005; neutral_panel +2.34 [+1.97, +2.72] p=0.0005; interaction +2.97 [+2.34, +3.56]
- **F.rec_score**: user_effect +0.16 [+0.11, +0.22] p=0.0020; panel_effect +0.26 [+0.16, +0.35] p=0.0005; neutral_panel +0.48 [+0.41, +0.56] p=0.0005; interaction +0.67 [+0.56, +0.78]
- **F.mentions_law**: user_effect +0.00 [+0.00, +0.00] p=1.0000; panel_effect +0.00 [+0.00, +0.00] p=1.0000; neutral_panel +0.00 [+0.00, +0.00] p=1.0000; interaction +0.00 [+0.00, +0.00]
- **F.reputation_warning**: user_effect -0.12 [-0.25, +0.00] p=0.1724; panel_effect -0.25 [-0.38, -0.11] p=0.0055; neutral_panel -0.50 [-0.69, -0.31] p=0.0005; interaction +0.06 [-0.16, +0.28]
- **F.warmth**: user_effect +0.66 [+0.48, +0.83] p=0.0005; panel_effect +0.41 [+0.27, +0.55] p=0.0005; neutral_panel +0.53 [+0.34, +0.69] p=0.0005; interaction +0.56 [+0.28, +0.91]
- **Gender inference check**: {"man/women": {"man": 8}, "woman/women": {"woman": 8}, "unstated/women": {"unknown": 2, "man": 2, "woman": 4}, "man/men": {"man": 8}, "woman/men": {"woman": 8}, "unstated/men": {"unknown": 3, "man": 4, "woman": 1}}

## Raters

```
{
 "agreement": {},
 "masking": {
  "claude-subscription": {
   "guessed": 103,
   "correct": 100,
   "unknown": 153
  }
 },
 "mirror_by_rater": {
  "claude-subscription rates claude-subscription (en)": 2.6875,
  "claude-subscription rates claude-subscription (is)": 2.5625
 }
}
```

## Coverage and interpretation

All 1,440 planned responses completed with zero execution errors in the
final data. All 960 structured recommendations and all 960 numerical
likelihoods parsed; there is no missingness in either primary outcome, by
cell or overall (see `coverage.json`). This is cleaner coverage than the
Codex subscription audit, which had substantial missing likelihood values
(67.7% in English, 98.1% in Icelandic, after the 9 October 2026 parser
correction) from selective refusal to give a number.

All 384 free-text replies were blind self-rated, with zero batch errors in
the final data. Masking was imperfect: the rater guessed the explicit user
sex in 103/384 replies, correctly in 100/103. A 72-reply human sample was
exported; no human ratings have been collected.

Collection was not a single pass: the account's usage-session cap (a
roughly 5-hour rolling window) was hit three times during the main run and
once during rating. Every capped call was retried after its stated reset
and is indistinguishable in the final data from a first-attempt success —
see METHODS.md for the operational detail. This means wall-clock collection
time for this audit (about a day) is not comparable to Codex's or
Antigravity's single-pass runs, but the response data themselves carry no
flag for which calls needed a retry.
