"""Builds the full, seeded run plan from the scenario files.

Cells: user gender U in {man, woman, unstated} x gender of the hired person
and the panel P in {men, women}. Arms: S (structured decision), F (free text),
G (gender-inference check, one per message, no replicates).
"""
import difflib
import itertools
import random

from .util import read_json, scenario_file, sha256_file, study_dir, write_json

USERS = ["man", "woman", "unstated"]
PANELS = ["men", "women"]


def render(spec, sc, u, p, arm):
    sl = spec["slots"]
    fields = {k: v[u] if k == "user_intro" else v[p] for k, v in sl.items()}
    fields.update(role=sc["role"], user_quals=sc["user_quals"], hired_quals=sc["hired_quals"])
    fields["hired_noun"] = sl["hired_noun"][p]
    q = spec["questions"]["F" if arm == "G" else arm].format(**fields)
    msg = spec["template"].format(question=q, **fields)
    if arm == "G":
        return spec["gender_check"].format(message=msg)
    return msg


def word_diff(a, b):
    aw, bw = a.split(), b.split()
    sm = difflib.SequenceMatcher(None, aw, bw)
    return [(" ".join(aw[i1:i2]), " ".join(bw[j1:j2])) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal"]


def build(cfg):
    st = cfg["study"]
    plan = []
    checks = []
    for lang in st["languages"]:
        spec = read_json(scenario_file(lang))
        for sc in spec["scenarios"]:
            arms = [("S", st["reps_S"]), ("F", st["reps_F"])] + ([("G", 1)] if st["gender_check"] else [])
            for arm, reps in arms:
                for u, p in itertools.product(USERS, PANELS):
                    msg = render(spec, sc, u, p, arm)
                    for r in range(1, reps + 1):
                        plan.append({"lang": lang, "scenario": sc["id"], "arm": arm, "U": u, "P": p,
                                     "rep": r, "system": spec["system_prompt"], "message": msg})
            # Sanity check: mirrored messages may differ only in gender words
            a = render(spec, sc, "man", "women", "F")
            b = render(spec, sc, "woman", "men", "F")
            checks.append({"lang": lang, "scenario": sc["id"], "mirror_diff": word_diff(a, b)})
    rng = random.Random(st["seed"])
    rng.shuffle(plan)
    for i, row in enumerate(plan, 1):
        row["plan_id"] = f"P{i:05d}"
    d = study_dir(cfg)
    write_json(d / "plan.json", plan)
    write_json(d / "mirror_checks.json", checks)
    manifest = {"plan.json": sha256_file(d / "plan.json")}
    for lang in st["languages"]:
        manifest[f"scenarios/{lang}.json"] = sha256_file(scenario_file(lang))
    write_json(d / "plan_manifest.json", manifest)
    return plan, checks, manifest
