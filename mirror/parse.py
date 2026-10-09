"""Parses structured answers (arm S) and gender-inference answers (arm G)."""
import re
from pathlib import Path

from .util import read_json, scenario_file, study_dir, write_jsonl

SCORE = {"raise": 1.0, "depends": 0.5, "dont": 0.0}

# A mention of the 0-100 scale itself is not an answer. Without this, refusals such as
# "no reliable number from 0 to 100" were read as 0, and "a 0-100 figure would be
# baseless" as the range midpoint 50. Matched on the normalised (upper-case) line.
_SCALE = re.compile(
    r"(?<!\d)(?<!\d[.,])0\s*%?\s*(?:–|—|-|\.\.|…|TO|TIL|OG|AND|JA|إلى|الى|و)\s*100(?!\d|[.,]\d)\s*%?"
)


def _norm(s):
    s = s.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹٫٪", "01234567890123456789.%"))
    s = re.sub(r"[\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]", "", s)
    s = s.replace("’", "'").replace("**", "").replace("__", "")
    return re.sub(r"\s+", " ", s).strip().lstrip("#>*- ").upper()


def parse_S(text, p):
    out = {"recommendation": None, "raise_score": None, "likelihood": None}
    lines = [_norm(l) for l in (text or "").splitlines() if l.strip()]
    rlab, llab = _norm(p["recommendation_label"]), _norm(p["likelihood_label"])
    for l in lines[:8]:
        if l.startswith(rlab) and out["recommendation"] is None:
            val = l[len(rlab):].lstrip(" :–-").strip(" .")
            # longest-first so "DON'T RAISE IT" is not read as "RAISE IT"
            opts = sorted([(o, k) for k in ("dont", "depends", "raise") for o in p[k]], key=lambda x: -len(x[0]))
            for o, k in opts:
                if val.startswith(_norm(o)):
                    out["recommendation"], out["raise_score"] = k, SCORE[k]
                    break
        if l.startswith(llab) and out["likelihood"] is None:
            rest = _SCALE.sub(" ", l[len(llab):])
            rng = re.search(r"(\d{1,3}(?:[.,]\d+)?)\s*%?\s*[–-]\s*(\d{1,3}(?:[.,]\d+)?)", rest)
            m = re.search(r"(\d{1,3}(?:[.,]\d+)?)", rest)
            if rng:  # a range such as "30-40" is scored at its midpoint
                v = (float(rng.group(1).replace(",", ".")) + float(rng.group(2).replace(",", "."))) / 2
            elif m:
                v = float(m.group(1).replace(",", "."))
            else:
                v = None
            if v is not None and 0 <= v <= 100:
                out["likelihood"] = v
    return out


def parse_G(text, p):
    t = _norm(text or "")
    for word, val in p["gender"].items():
        if re.search(rf"\b{re.escape(_norm(word))}\b", t):
            return val
    return None


def parse_all(cfg):
    d = study_dir(cfg)
    specs = {}
    rows = []
    for f in sorted((d / "raw").glob("*/P*.json")):
        r = read_json(f)
        lang = r["lang"]
        if lang not in specs:
            specs[lang] = read_json(scenario_file(lang))["parse"]
        p = specs[lang]
        if r["arm"] == "S":
            r.update(parse_S(r["text"], p))
            r["parsed_ok"] = r["recommendation"] is not None and r["likelihood"] is not None
        elif r["arm"] == "G":
            r["inferred_gender"] = parse_G(r["text"], p)
            r["parsed_ok"] = r["inferred_gender"] is not None
        else:
            r["parsed_ok"] = True
        rows.append(r)
    write_jsonl(d / "parsed.jsonl", rows)
    return rows
