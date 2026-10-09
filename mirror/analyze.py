"""Preregistered analysis. Every estimate is a scenario-weighted average of
within-scenario contrasts; uncertainty comes from resampling scenarios
(cluster bootstrap); p-values from permuting labels within scenario.

Key contrasts (cells are user U x panel P):
  mirror       = (woman, men) - (man, women)       <- primary
  user_effect  = mean over P of (woman - man)
  panel_effect = mean over U in {man, woman} of (men - women)
  mirror = user_effect + panel_effect (exact identity)
  neutral_panel = (unstated, men) - (unstated, women)
  interaction  = [(woman,men)-(man,men)] - [(woman,women)-(man,women)]
"""
import glob
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from .util import read_json, read_jsonl, study_dir, write_json

CELLS = [("man", "women"), ("woman", "women"), ("unstated", "women"), ("man", "men"), ("woman", "men"), ("unstated", "men")]
REC = {"raise": 1.0, "conditional": 0.5, "dont": 0.0}

CONTRASTS = {
    "mirror": {("woman", "men"): 1, ("man", "women"): -1},
    "user_effect": {("woman", "men"): .5, ("man", "men"): -.5, ("woman", "women"): .5, ("man", "women"): -.5},
    "panel_effect": {("man", "men"): .5, ("man", "women"): -.5, ("woman", "men"): .5, ("woman", "women"): -.5},
    "interaction": {("woman", "men"): 1, ("man", "men"): -1, ("woman", "women"): -1, ("man", "women"): 1},
    "neutral_panel": {("unstated", "men"): 1, ("unstated", "women"): -1},
}
# Which labels are exchangeable under the null for each contrast (permuted within these strata)
PERM = {"mirror": "pair", "neutral_panel": "pair", "user_effect": "U", "panel_effect": "P", "interaction": None}


def _scenario_contrast(by_cell, weights):
    vals = []
    for c, w in weights.items():
        x = by_cell.get(c)
        if not x:
            return None
        vals.append(w * float(np.mean(x)))
    return sum(vals)


def estimate(rows, outcome, weights):
    """rows: dicts with scenario, U, P, outcome. Returns scenario-averaged contrast."""
    by_s = defaultdict(lambda: defaultdict(list))
    for r in rows:
        v = r.get(outcome)
        if v is not None:
            by_s[r["scenario"]][(r["U"], r["P"])].append(v)
    per = {s: _scenario_contrast(cells, weights) for s, cells in by_s.items()}
    per = {s: v for s, v in per.items() if v is not None}
    return (float(np.mean(list(per.values()))) if per else None), per, by_s


def bootstrap(per, B, rng, alpha=0.05):
    s = list(per)
    if len(s) < 2:
        return [None, None], [None, None]
    vals = np.array([per[k] for k in s])
    idx = rng.integers(0, len(s), size=(B, len(s)))
    boots = vals[idx].mean(axis=1)
    return ([float(np.quantile(boots, alpha / 2)), float(np.quantile(boots, 1 - alpha / 2))],
            [float(np.quantile(boots, 0.05)), float(np.quantile(boots, 0.95))])


def permutation_p(by_s, weights, kind, n, rng):
    obs_cells = {s: {c: list(v) for c, v in cells.items()} for s, cells in by_s.items()}

    def stat(cells_by_s):
        vals = [_scenario_contrast(c, weights) for c in cells_by_s.values()]
        vals = [v for v in vals if v is not None]
        return float(np.mean(vals)) if vals else 0.0

    obs = stat(obs_cells)
    if kind == "pair":
        groups = [list(weights)]
    elif kind == "U":
        groups = [[c for c in weights if c[1] == p] for p in ("men", "women")]
    else:
        groups = [[c for c in weights if c[0] == u] for u in ("man", "woman")]
    count = 0
    for _ in range(n):
        perm = {}
        for s, cells in obs_cells.items():
            new = dict(cells)
            for g in groups:
                pool = [x for c in g for x in cells.get(c, [])]
                rng.shuffle(pool)
                i = 0
                for c in g:
                    k = len(cells.get(c, []))
                    new[c] = pool[i:i + k]
                    i += k
            perm[s] = new
        if abs(stat(perm)) >= abs(obs) - 1e-12:
            count += 1
    return (count + 1) / (n + 1)


def holm(pvals):
    items = sorted([(p, k) for k, p in pvals.items() if p is not None])
    m = len(items)
    adj, running = {}, 0.0
    for i, (p, k) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))
        adj[k] = running
    return adj


def cell_table(rows, outcome):
    t = {}
    for u, p in CELLS:
        x = [r[outcome] for r in rows if r["U"] == u and r["P"] == p and r.get(outcome) is not None]
        n_all = sum(1 for r in rows if r["U"] == u and r["P"] == p)
        t[f"{u}/{p}"] = {"mean": float(np.mean(x)) if x else None, "n": len(x), "n_missing": n_all - len(x)}
    return t


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return None
    ra, rb = _rank(a), _rank(b)
    if ra.std() == 0 or rb.std() == 0:
        return None
    return float(np.corrcoef(ra, rb)[0, 1])


def _rank(x):
    order = x.argsort()
    r = np.empty(len(x))
    r[order] = np.arange(len(x))
    for v in np.unique(x):
        m = x == v
        r[m] = r[m].mean()
    return r


def kappa(a, b, weighted_levels=None):
    a, b = list(a), list(b)
    if not a:
        return None
    if weighted_levels:
        cats = weighted_levels
        idx = {c: i for i, c in enumerate(cats)}
        k = len(cats)
        O = np.zeros((k, k))
        for x, y in zip(a, b):
            O[idx[x], idx[y]] += 1
        W = np.array([[((i - j) ** 2) / ((k - 1) ** 2) for j in range(k)] for i in range(k)])
        E = np.outer(O.sum(1), O.sum(0)) / O.sum()
        den = (W * E).sum()
        return float(1 - (W * O).sum() / den) if den else None
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return float((po - pe) / (1 - pe)) if pe < 1 else None


def load(cfg):
    d = study_dir(cfg)
    rows = read_jsonl(d / "parsed.jsonl")
    keymap_path = d / "ratings" / "_keymap.json"
    ratings = []
    if keymap_path.exists():
        keymap = read_json(keymap_path)
        for f in sorted(glob.glob(str(d / "ratings" / "*.json"))):
            if Path(f).name.startswith("_"):
                continue
            for r in read_json(f):
                k = keymap.get(r["code_id"])
                if k:
                    ratings.append({**r, **k})
    return rows, ratings


def attach_ratings(rows, ratings):
    llm = defaultdict(list)
    for r in ratings:
        if not str(r.get("rater", "")).startswith("human:"):
            llm[(r["model_id"], r["plan_id"])].append(r)
    for r in rows:
        if r["arm"] != "F":
            continue
        rs = llm.get((r["model_id"], r["plan_id"]), [])
        if not rs:
            continue
        r["net_legitimacy"] = float(np.mean([x["legitimacy"] - x["dismissal"] for x in rs]))
        r["legitimacy"] = float(np.mean([x["legitimacy"] for x in rs]))
        r["dismissal"] = float(np.mean([x["dismissal"] for x in rs]))
        r["rec_score"] = float(np.mean([REC[x["recommendation"]] for x in rs]))
        r["mentions_law"] = float(np.mean([x["mentions_law"] for x in rs]))
        r["reputation_warning"] = float(np.mean([x["reputation_warning"] for x in rs]))
        r["warmth"] = float(np.mean([x["warmth"] for x in rs]))
        r["n_raters"] = len(rs)


def analyze(cfg):
    a = cfg["analysis"]
    rng = np.random.default_rng(cfg["study"]["seed"])
    rows, ratings = load(cfg)
    attach_ratings(rows, ratings)
    res = {"n_rows": len(rows), "groups": {}, "notes": []}
    if cfg["study"].get("exploratory"):
        res["exploratory"] = True
        res["notes"].append("Separate exploratory audit; not the preregistered API study.")
    if cfg["study"].get("method_note"):
        res["notes"].append(cfg["study"]["method_note"])
    groups = sorted({(r["model_id"], r["lang"]) for r in rows})
    primary_p = {}
    outcomes = {"S": [("raise_score", a["equivalence_raise"]), ("likelihood", a["equivalence_likelihood"])],
                "F": [("net_legitimacy", a["equivalence_net_legitimacy"]), ("rec_score", a["equivalence_raise"]),
                      ("mentions_law", None), ("reputation_warning", None), ("warmth", None)]}
    for mid, lang in groups:
        g = {}
        for arm, outs in outcomes.items():
            sub = [r for r in rows if r["model_id"] == mid and r["lang"] == lang and r["arm"] == arm]
            if not sub:
                continue
            for outcome, eq in outs:
                if not any(r.get(outcome) is not None for r in sub):
                    continue
                entry = {"cells": cell_table(sub, outcome), "contrasts": {}}
                for name, w in CONTRASTS.items():
                    est, per, by_s = estimate(sub, outcome, w)
                    if est is None:
                        continue
                    ci95, ci90 = bootstrap(per, a["bootstrap"], rng)
                    # Full permutation count for the primary contrast; fewer for secondary ones
                    n_perm = a["permutations"] if (arm == "S" and name == "mirror") else min(2000, a["permutations"])
                    p = permutation_p(by_s, w, PERM[name], n_perm, rng) if PERM[name] else None
                    c = {"estimate": est, "ci95": ci95, "p": p, "n_scenarios": len(per)}
                    if eq is not None and ci90[0] is not None:
                        c["equivalence_bound"] = eq
                        c["ci90"] = ci90
                        c["equivalent"] = bool(-eq < ci90[0] and ci90[1] < eq)
                    entry["contrasts"][name] = c
                    if arm == "S" and name == "mirror":
                        primary_p[f"{mid}|{lang}|{outcome}"] = p
                g[f"{arm}.{outcome}"] = entry
        # Gender-inference check
        gsub = [r for r in rows if r["model_id"] == mid and r["lang"] == lang and r["arm"] == "G"]
        if gsub:
            g["G.inferred_gender"] = {f"{u}/{p}": dict(Counter(r.get("inferred_gender") for r in gsub if r["U"] == u and r["P"] == p)) for u, p in CELLS}
        res["groups"][f"{mid}|{lang}"] = g
    adj = holm(primary_p)
    for k, p in adj.items():
        mid, lang, outcome = k.split("|")
        res["groups"][f"{mid}|{lang}"][f"S.{outcome}"]["contrasts"]["mirror"]["p_holm"] = p
    res["primary_family_size"] = len(primary_p)

    # Cross-model differences in the primary contrast, paired by scenario
    res["cross_model"] = {}
    for lang in sorted({l for _, l in groups}):
        mids = sorted({m for m, l in groups if l == lang})
        for outcome in ("raise_score", "likelihood"):
            per_model = {}
            for m in mids:
                sub = [r for r in rows if r["model_id"] == m and r["lang"] == lang and r["arm"] == "S"]
                est, per, _ = estimate(sub, outcome, CONTRASTS["mirror"])
                if est is not None:
                    per_model[m] = per
            for m1, m2 in itertools.combinations(sorted(per_model), 2):
                common = sorted(set(per_model[m1]) & set(per_model[m2]))
                if len(common) < 2:
                    continue
                diff = {s: per_model[m1][s] - per_model[m2][s] for s in common}
                ci95, _ = bootstrap(diff, a["bootstrap"], rng)
                res["cross_model"][f"{lang}|{outcome}|{m1} - {m2}"] = {"estimate": float(np.mean(list(diff.values()))), "ci95": ci95}

    # Raters: agreement, self-preference, masking
    res["raters"] = rater_checks(rows, ratings)
    write_json(study_dir(cfg) / "results.json", res)
    report(cfg, res)
    return res


def rater_checks(rows, ratings):
    out = {}
    by_item = defaultdict(dict)
    for r in ratings:
        by_item[(r["model_id"], r["plan_id"])][r["rater"]] = r
    raters = sorted({r["rater"] for r in ratings})
    pairs = {}
    for r1, r2 in itertools.combinations(raters, 2):
        both = [(v[r1], v[r2]) for v in by_item.values() if r1 in v and r2 in v]
        if len(both) < 5:
            continue
        pairs[f"{r1} ~ {r2}"] = {
            "n": len(both),
            "legitimacy_kappa_w": kappa([x["legitimacy"] for x, _ in both], [y["legitimacy"] for _, y in both], [1, 2, 3, 4, 5]),
            "dismissal_kappa_w": kappa([x["dismissal"] for x, _ in both], [y["dismissal"] for _, y in both], [1, 2, 3, 4, 5]),
            "recommendation_kappa": kappa([x["recommendation"] for x, _ in both], [y["recommendation"] for _, y in both]),
            "net_spearman": spearman([x["legitimacy"] - x["dismissal"] for x, _ in both], [y["legitimacy"] - y["dismissal"] for _, y in both]),
        }
    out["agreement"] = pairs
    # Masking leak: can raters tell the user's gender?
    cell = {(r["model_id"], r["plan_id"]): r for r in rows if r["arm"] == "F"}
    leak = defaultdict(lambda: Counter())
    for r in ratings:
        row = cell.get((r["model_id"], r["plan_id"]))
        if not row or row["U"] == "unstated":
            continue
        g = r.get("gender_guess")
        if g in ("man", "woman"):
            leak[r["rater"]]["guessed"] += 1
            leak[r["rater"]]["correct"] += int(g == row["U"])
        else:
            leak[r["rater"]]["unknown"] += 1
    out["masking"] = {k: dict(v) for k, v in leak.items()}
    # Per-rater primary F contrast by generating model (self-preference check)
    sp = {}
    for rater in raters:
        for mid in sorted({r["model_id"] for r in rows}):
            sub = []
            for r in rows:
                if r["arm"] != "F" or r["model_id"] != mid:
                    continue
                x = by_item.get((mid, r["plan_id"]), {}).get(rater)
                if x:
                    sub.append({**r, "net_r": x["legitimacy"] - x["dismissal"]})
            for lang in sorted({r["lang"] for r in sub}):
                est, _, _ = estimate([r for r in sub if r["lang"] == lang], "net_r", CONTRASTS["mirror"])
                if est is not None:
                    sp[f"{rater} rates {mid} ({lang})"] = est
    out["mirror_by_rater"] = sp
    return out


def fmt(x, d=2):
    if x is None:
        return "–"
    return f"{x:+.{d}f}" if isinstance(x, float) else str(x)


def report(cfg, res):
    d = study_dir(cfg)
    L = [f"# Mirror audit: {cfg['study']['name']}", "",
         "Contrasts are scenario-weighted. 95% CIs from a cluster bootstrap over scenarios; p from within-scenario permutation. "
         "Primary: mirror contrast on arm S outcomes, Holm-adjusted across models and languages.", ""]
    if res.get("notes"):
        L[2:2] = [" ".join(res["notes"]), ""]
    for gk, g in res["groups"].items():
        mid, lang = gk.split("|")
        L.append(f"## {mid} ({lang})")
        L.append("")
        L.append("| Outcome | man/women | woman/men | unstated/women | unstated/men | man/men | woman/women | Mirror (95% CI) | p | p Holm | Equivalent? |")
        L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for ok, e in g.items():
            if ok.startswith("G."):
                continue
            c = e["cells"]
            mr = e["contrasts"].get("mirror", {})
            ci = mr.get("ci95", [None, None])
            row = [ok] + [fmt(c[k]["mean"]) for k in ("man/women", "woman/men", "unstated/women", "unstated/men", "man/men", "woman/women")]
            row += [f"{fmt(mr.get('estimate'))} ({fmt(ci[0])} to {fmt(ci[1])})", f"{mr.get('p', float('nan')):.4f}" if mr.get("p") is not None else "–",
                    f"{mr['p_holm']:.4f}" if "p_holm" in mr else "", {True: "yes", False: "no"}.get(mr.get("equivalent"), "")]
            L.append("| " + " | ".join(row) + " |")
        L.append("")
        for ok, e in g.items():
            if ok.startswith("G."):
                continue
            parts = []
            for name in ("user_effect", "panel_effect", "neutral_panel", "interaction"):
                c = e["contrasts"].get(name)
                if c:
                    pv = f" p={c['p']:.4f}" if c.get("p") is not None else ""
                    parts.append(f"{name} {fmt(c['estimate'])} [{fmt(c['ci95'][0])}, {fmt(c['ci95'][1])}]{pv}")
            if parts:
                L.append(f"- **{ok}**: " + "; ".join(parts))
        if "G.inferred_gender" in g:
            L.append(f"- **Gender inference check**: {json.dumps(g['G.inferred_gender'], ensure_ascii=False)}")
        L.append("")
    if res["cross_model"]:
        L += ["## Cross-model differences in the mirror contrast", "", "| Comparison | Difference (95% CI) |", "| --- | --- |"]
        for k, v in res["cross_model"].items():
            L.append(f"| {k} | {fmt(v['estimate'])} ({fmt(v['ci95'][0])} to {fmt(v['ci95'][1])}) |")
        L.append("")
    r = res["raters"]
    L += ["## Raters", "", "```", json.dumps(r, ensure_ascii=False, indent=1), "```", ""]
    (d / "report.md").write_text("\n".join(L), encoding="utf-8")
    try:
        figure(cfg, res)
    except Exception as e:  # noqa: BLE001
        res["notes"].append(f"figure skipped: {e}")


def figure(cfg, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    labels, est, lo, hi, panels = [], [], [], [], []
    for gk, g in res["groups"].items():
        for outcome, scale in (("S.raise_score", 1.0), ("S.likelihood", 1.0)):
            mr = g.get(outcome, {}).get("contrasts", {}).get("mirror")
            if mr and mr["ci95"][0] is not None:
                labels.append(gk.replace("|", " · "))
                est.append(mr["estimate"] / scale)
                lo.append(mr["ci95"][0] / scale)
                hi.append(mr["ci95"][1] / scale)
                panels.append(outcome)
    if not labels:
        return
    n_rows = max(len([p for p in panels if p == "S.raise_score"]), 1)
    fig, axes = plt.subplots(1, 2, figsize=(11, 0.55 * n_rows + 2.2), sharey=False)
    for ax, outcome, title, lim in zip(axes, ("S.raise_score", "S.likelihood"),
                                       ("Recommendation to raise it (score 0–1)", "Stated likelihood that sex mattered (points, 0–100)"), (1.0, 100.0)):
        idx = [i for i, p in enumerate(panels) if p == outcome]
        y = np.arange(len(idx))
        ax.errorbar([est[i] for i in idx], y, xerr=[[est[i] - lo[i] for i in idx], [hi[i] - est[i] for i in idx]], fmt="o", color="#2f6fdf", capsize=3)
        ax.axvline(0, color="#888", lw=1)
        ax.set_xlim(-lim * 0.6, lim * 0.6)
        ax.set_ylim(-0.7, len(idx) - 0.3)
        ax.set_yticks(y, [labels[i] for i in idx])
        ax.set_title(title, fontsize=10)
    fig.supxlabel("Mirror contrast with 95% CI: woman asking about an all-male panel minus man asking about an all-female panel (positive = more support for the woman)", fontsize=9)
    fig.tight_layout()
    fig.savefig(study_dir(cfg) / "mirror_contrast.png", dpi=160)
