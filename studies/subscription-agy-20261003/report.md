# Mirror audit: subscription-agy-20261003

Separate exploratory audit; not the preregistered API study. Antigravity CLI (agy) 1.2.16; requested gemini-3.8-flash-high; fresh ephemeral sessions in temporary directories; minimal model instructions via GEMINI.md; slash commands and skills disabled. Free-text ratings use one blind self-rater; no independent or human validation. See METHODS.md.

Contrasts are scenario-weighted. 95% CIs from a cluster bootstrap over scenarios; p from within-scenario permutation. Primary: mirror contrast on arm S outcomes, Holm-adjusted across models and languages.

## agy-subscription (en)

| Outcome | man/women | woman/men | unstated/women | unstated/men | man/men | woman/women | Mirror (95% CI) | p | p Holm | Equivalent? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S.raise_score | +0.01 | +0.49 | +0.00 | +0.47 | +0.00 | +0.00 | +0.48 (+0.46 to +0.50) | 0.0001 | 0.0004 | no |
| S.likelihood | +21.06 | +48.50 | +19.38 | +47.19 | +0.75 | +1.94 | +27.44 (+25.31 to +29.75) | 0.0001 | 0.0004 | no |
| F.net_legitimacy | -3.62 | +1.50 | -3.81 | +1.12 | -3.00 | -3.88 | +5.12 (+4.69 to +5.53) | 0.0005 |  | no |
| F.rec_score | +0.03 | +0.48 | +0.02 | +0.48 | +0.09 | +0.00 | +0.45 (+0.38 to +0.53) | 0.0005 |  | no |
| F.mentions_law | +0.53 | +0.97 | +0.25 | +1.00 | +0.62 | +0.41 | +0.44 (+0.31 to +0.59) | 0.0005 |  |  |
| F.reputation_warning | +1.00 | +0.47 | +1.00 | +0.44 | +0.75 | +0.72 | -0.53 (-0.75 to -0.31) | 0.0005 |  |  |
| F.warmth | +2.97 | +3.53 | +2.91 | +3.59 | +2.34 | +2.66 | +0.56 (+0.34 to +0.78) | 0.0005 |  |  |

- **S.raise_score**: user_effect +0.24 [+0.23, +0.25] p=0.0005; panel_effect +0.24 [+0.23, +0.25] p=0.0005; neutral_panel +0.47 [+0.41, +0.50] p=0.0005; interaction +0.49 [+0.46, +0.52]
- **S.likelihood**: user_effect +14.31 [+13.16, +15.66] p=0.0005; panel_effect +13.12 [+12.00, +14.25] p=0.0005; neutral_panel +27.81 [+24.00, +32.06] p=0.0005; interaction +66.88 [+61.50, +71.44]
- **F.net_legitimacy**: user_effect +2.12 [+1.78, +2.45] p=0.0005; panel_effect +3.00 [+2.61, +3.41] p=0.0005; neutral_panel +4.94 [+4.25, +5.50] p=0.0005; interaction +4.75 [+3.94, +5.47]
- **F.rec_score**: user_effect +0.18 [+0.13, +0.22] p=0.0005; panel_effect +0.27 [+0.22, +0.34] p=0.0005; neutral_panel +0.47 [+0.39, +0.53] p=0.0005; interaction +0.42 [+0.36, +0.48]
- **F.mentions_law**: user_effect +0.11 [-0.05, +0.25] p=0.1934; panel_effect +0.33 [+0.14, +0.52] p=0.0005; neutral_panel +0.75 [+0.62, +0.88] p=0.0005; interaction +0.47 [+0.06, +0.88]
- **F.reputation_warning**: user_effect -0.28 [-0.39, -0.14] p=0.0005; panel_effect -0.25 [-0.44, -0.06] p=0.0015; neutral_panel -0.56 [-0.78, -0.34] p=0.0005; interaction +0.00 [-0.41, +0.38]
- **F.warmth**: user_effect +0.44 [+0.20, +0.69] p=0.0005; panel_effect +0.12 [+0.02, +0.23] p=0.3543; neutral_panel +0.69 [+0.34, +0.94] p=0.0010; interaction +1.50 [+1.03, +1.94]
- **Gender inference check**: {"man/women": {"man": 8}, "woman/women": {"woman": 8}, "unstated/women": {"unknown": 8}, "man/men": {"man": 8}, "woman/men": {"woman": 8}, "unstated/men": {"unknown": 8}}

## agy-subscription (is)

| Outcome | man/women | woman/men | unstated/women | unstated/men | man/men | woman/women | Mirror (95% CI) | p | p Holm | Equivalent? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S.raise_score | +0.35 | +0.84 | +0.31 | +0.86 | +0.03 | +0.01 | +0.49 (+0.47 to +0.51) | 0.0001 | 0.0004 | no |
| S.likelihood | +31.62 | +68.88 | +30.38 | +67.06 | +0.25 | +0.25 | +37.25 (+32.88 to +41.62) | 0.0001 | 0.0004 | no |
| F.net_legitimacy | -0.66 | +3.34 | -0.78 | +3.38 | -1.34 | -3.41 | +4.00 (+3.00 to +5.06) | 0.0005 |  | no |
| F.rec_score | +0.39 | +0.92 | +0.36 | +0.91 | +0.23 | +0.03 | +0.53 (+0.39 to +0.66) | 0.0005 |  | no |
| F.mentions_law | +1.00 | +1.00 | +1.00 | +1.00 | +1.00 | +1.00 | +0.00 (+0.00 to +0.00) | 1.0000 |  |  |
| F.reputation_warning | +0.12 | +0.00 | +0.22 | +0.00 | +0.16 | +0.16 | -0.12 (-0.31 to +0.00) | 0.0710 |  |  |
| F.warmth | +3.03 | +3.25 | +2.97 | +3.16 | +2.53 | +2.25 | +0.22 (-0.03 to +0.47) | 0.1754 |  |  |

- **S.raise_score**: user_effect +0.24 [+0.22, +0.25] p=0.0005; panel_effect +0.26 [+0.24, +0.28] p=0.0005; neutral_panel +0.55 [+0.49, +0.61] p=0.0005; interaction +1.16 [+0.88, +1.38]
- **S.likelihood**: user_effect +18.62 [+16.34, +20.94] p=0.0005; panel_effect +18.62 [+16.41, +20.78] p=0.0005; neutral_panel +36.69 [+30.81, +41.94] p=0.0005; interaction +100.00 [+88.44, +111.75]
- **F.net_legitimacy**: user_effect +0.97 [+0.12, +1.83] p=0.0290; panel_effect +3.03 [+2.58, +3.55] p=0.0005; neutral_panel +4.16 [+2.97, +5.22] p=0.0005; interaction +7.44 [+6.59, +8.19]
- **F.rec_score**: user_effect +0.16 [+0.05, +0.28] p=0.0115; panel_effect +0.37 [+0.31, +0.43] p=0.0005; neutral_panel +0.55 [+0.44, +0.64] p=0.0005; interaction +1.05 [+0.86, +1.22]
- **F.mentions_law**: user_effect +0.00 [+0.00, +0.00] p=1.0000; panel_effect +0.00 [+0.00, +0.00] p=1.0000; neutral_panel +0.00 [+0.00, +0.00] p=1.0000; interaction +0.00 [+0.00, +0.00]
- **F.reputation_warning**: user_effect -0.06 [-0.17, +0.03] p=0.3263; panel_effect -0.06 [-0.17, +0.02] p=0.3283; neutral_panel -0.22 [-0.50, +0.00] p=0.0040; interaction -0.19 [-0.50, +0.03]
- **F.warmth**: user_effect -0.03 [-0.23, +0.14] p=0.9035; panel_effect +0.25 [+0.09, +0.39] p=0.0480; neutral_panel +0.19 [-0.09, +0.47] p=0.3193; interaction +1.50 [+1.12, +1.88]
- **Gender inference check**: {"man/women": {"man": 8}, "woman/women": {"woman": 8}, "unstated/women": {"unknown": 8}, "man/men": {"man": 8}, "woman/men": {"woman": 8}, "unstated/men": {"unknown": 8}}

## Raters

```
{
 "agreement": {},
 "masking": {
  "agy-subscription": {
   "unknown": 151,
   "guessed": 105,
   "correct": 103
  }
 },
 "mirror_by_rater": {
  "agy-subscription rates agy-subscription (en)": 5.125,
  "agy-subscription rates agy-subscription (is)": 4.0
 }
}
```
## Coverage and interpretation

All 1,440 planned responses completed with zero execution errors. All 960 structured recommendations and numerical likelihood estimates parsed successfully with 0 missing values across all cells in both English and Icelandic (100% structured completeness; see coverage.json).

All 384 free-text replies were blind self-rated, with zero batch errors. Masking was imperfect: the rater guessed the explicit user sex in 105/256 replies, correctly in 103. Free-text findings require independent validation. A 72-reply human sample was exported; no human ratings have been collected.
