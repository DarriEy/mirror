# Mirror audit: subscription-codex-ar-20261004

Separate exploratory audit; not the preregistered API study. Arabic exploratory extension via Codex subscription requesting gpt-6-astra, with the same repetitions and pipeline as the English/Icelandic audit. Modern Standard Arabic translation has no independent native-speaker validation. Arabic gender morphology makes masking imperfect. One blind self-rater; no independent or human validation. See METHODS.md.

Contrasts are scenario-weighted. 95% CIs from a cluster bootstrap over scenarios; p from within-scenario permutation. Primary: mirror contrast on arm S outcomes, Holm-adjusted across models and languages.

## codex-subscription (ar)

| Outcome | man/women | woman/men | unstated/women | unstated/men | man/men | woman/women | Mirror (95% CI) | p | p Holm | Equivalent? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S.raise_score | +0.42 | +0.97 | +0.34 | +0.90 | +0.50 | +0.00 | +0.54 (+0.51 to +0.58) | 0.0001 | 0.0001 | no |
| S.likelihood | +50.00 | +40.00 | – | +50.00 | +10.00 | +14.00 | – (– to –) | – |  |  |
| F.net_legitimacy | -0.97 | +1.09 | -0.97 | +1.22 | -0.75 | -1.94 | +2.06 (+1.72 to +2.41) | 0.0005 |  | no |
| F.rec_score | +0.67 | +1.00 | +0.62 | +1.00 | +0.80 | +0.48 | +0.33 (+0.19 to +0.48) | 0.0005 |  | no |
| F.mentions_law | +0.62 | +0.81 | +0.66 | +0.78 | +0.75 | +0.75 | +0.19 (+0.06 to +0.34) | 0.0685 |  |  |
| F.reputation_warning | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 (+0.00 to +0.00) | 1.0000 |  |  |
| F.warmth | +3.06 | +3.06 | +3.16 | +3.00 | +2.56 | +2.50 | +0.00 (-0.16 to +0.19) | 1.0000 |  |  |

- **S.raise_score**: user_effect +0.02 [-0.00, +0.04] p=0.5037; panel_effect +0.52 [+0.50, +0.54] p=0.0005; neutral_panel +0.56 [+0.50, +0.63] p=0.0005; interaction +0.89 [+0.82, +0.95]
- **F.net_legitimacy**: user_effect +0.44 [+0.19, +0.73] p=0.0160; panel_effect +1.62 [+1.36, +1.88] p=0.0005; neutral_panel +2.19 [+2.00, +2.41] p=0.0005; interaction +2.81 [+2.47, +3.28]
- **F.rec_score**: user_effect +0.01 [-0.09, +0.12] p=1.0000; panel_effect +0.32 [+0.27, +0.37] p=0.0005; neutral_panel +0.38 [+0.28, +0.45] p=0.0005; interaction +0.39 [+0.28, +0.48]
- **F.mentions_law**: user_effect +0.09 [+0.03, +0.16] p=0.1604; panel_effect +0.09 [+0.00, +0.20] p=0.1564; neutral_panel +0.12 [+0.00, +0.25] p=0.3333; interaction -0.06 [-0.34, +0.28]
- **F.reputation_warning**: user_effect +0.00 [+0.00, +0.00] p=1.0000; panel_effect +0.00 [+0.00, +0.00] p=1.0000; neutral_panel +0.00 [+0.00, +0.00] p=1.0000; interaction +0.00 [+0.00, +0.00]
- **F.warmth**: user_effect -0.03 [-0.16, +0.09] p=0.8621; panel_effect +0.03 [-0.09, +0.16] p=0.8751; neutral_panel -0.16 [-0.38, +0.03] p=0.1529; interaction +1.06 [+0.81, +1.38]
- **Gender inference check**: {"man/women": {"man": 8}, "woman/women": {"woman": 8}, "unstated/women": {"unknown": 8}, "man/men": {"man": 8}, "woman/men": {"woman": 8}, "unstated/men": {"unknown": 8}}

## Raters

```
{
 "agreement": {},
 "masking": {
  "codex-subscription": {
   "unknown": 10,
   "guessed": 118,
   "correct": 118
  }
 },
 "mirror_by_rater": {
  "codex-subscription rates codex-subscription (ar)": 2.0625
 }
}
```

## Coverage and interpretation

All 480 structured recommendations parsed. A numerical likelihood was given in only 25/480 structured replies; the rest declined to give one, so likelihood contrasts cannot be estimated for this language.

**Parser correction (9 October 2026).** The first version of the parser read refusals to give a likelihood, such as "no reliable number from 0 to 100", as 0, and "a 0-100 figure would be baseless" as the range midpoint 50. The parser now ignores mentions of the 0-100 scale itself. Recommendations were unaffected; this report, parsed.jsonl and results.json were regenerated from the unchanged raw replies.
