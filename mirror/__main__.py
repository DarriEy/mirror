"""Command line: python -m mirror <command> --config config.toml

  build                          make the seeded run plan and its fingerprint
  selftest [--models a,b]        one tiny call per configured model
  run --models a,b [--arms S,F,G] [--langs en,is] [--limit-scenarios N] [--max-reps N]
  export-manual --out prompts.csv [--arms S] [--langs en] [--max-reps 1]
  import-manual --model ID --file responses.csv
  parse                          parse structured answers and gender checks
  rate [--raters a,b]            blind model rating of free-text answers
  export-human --out sheet.csv   stratified sample for human raters
  import-human --file sheet.csv --name NAME
  analyze                        statistics, report.md, results.json, figure
  all --models a,b               build (if needed), run, parse, rate, analyze
"""
import argparse
import json

from . import analyze as A
from . import build as B
from . import parse as P
from . import rate as R
from . import run as X
from .util import load_config, study_dir


def csv_list(s):
    return [x.strip() for x in s.split(",") if x.strip()] if s else None


def main():
    ap = argparse.ArgumentParser(prog="mirror", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command")
    ap.add_argument("--config", default="config.toml")
    ap.add_argument("--models")
    ap.add_argument("--raters")
    ap.add_argument("--arms")
    ap.add_argument("--langs")
    ap.add_argument("--limit-scenarios", type=int)
    ap.add_argument("--max-reps", type=int)
    ap.add_argument("--out")
    ap.add_argument("--file")
    ap.add_argument("--model")
    ap.add_argument("--name")
    a = ap.parse_args()
    cfg = load_config(a.config)
    d = study_dir(cfg)

    if a.command in ("build", "all"):
        if a.command == "build" or not (d / "plan.json").exists():
            plan, checks, manifest = B.build(cfg)
            print(f"plan: {len(plan)} prompts per model -> {d / 'plan.json'}")
            bad = [c for c in checks if any(not _is_gender_pair(x, y) for x, y in c["mirror_diff"])]
            print("mirror check:", "only gender words differ" if not bad else f"CHECK THESE: {bad}")
            print("fingerprint (sha256 of plan.json):", manifest["plan.json"])
        if a.command == "build":
            return
    if a.command == "selftest":
        for k, v in X.selftest(cfg, csv_list(a.models)).items():
            print(f"{k}: {v}")
        return
    if a.command in ("run", "all"):
        for mid in csv_list(a.models) or [m["id"] for m in cfg["models"]]:
            X.run_model(cfg, mid, csv_list(a.arms), csv_list(a.langs), a.limit_scenarios, a.max_reps)
        if a.command == "run":
            return
    if a.command == "export-manual":
        n = X.export_manual(cfg, csv_list(a.arms) or ["S"], csv_list(a.langs), a.max_reps or 1, a.out or "manual_prompts.csv")
        print(f"wrote {n} prompts to {a.out or 'manual_prompts.csv'}")
        return
    if a.command == "import-manual":
        print(f"imported {X.import_manual(cfg, a.model, a.file)} responses as model '{a.model}'")
        return
    if a.command in ("parse", "all"):
        rows = P.parse_all(cfg)
        s = [r for r in rows if r["arm"] == "S"]
        print(f"parsed {len(rows)} responses; structured answers readable: {sum(r['parsed_ok'] for r in s)}/{len(s)}")
        if a.command == "parse":
            return
    if a.command in ("rate", "all"):
        print(json.dumps(R.rate_all(cfg, csv_list(a.raters)), indent=1))
        if a.command == "rate":
            return
    if a.command == "export-human":
        print(f"wrote {R.export_human(cfg, a.out or 'human_sheet.csv')} rows to {a.out or 'human_sheet.csv'}")
        return
    if a.command == "import-human":
        print(f"imported {R.import_human(cfg, a.file, a.name)} human ratings")
        return
    if a.command in ("analyze", "all"):
        res = A.analyze(cfg)
        print(f"wrote {d / 'report.md'} and {d / 'results.json'}")
        for gk, g in res["groups"].items():
            for ok in ("S.raise_score", "S.likelihood"):
                mr = g.get(ok, {}).get("contrasts", {}).get("mirror")
                if mr:
                    print(f"  {gk} {ok}: mirror {mr['estimate']:+.3f} 95% CI [{mr['ci95'][0]}, {mr['ci95'][1]}] p={mr['p']:.4f}")
        return
    if a.command not in ("all",):
        ap.error(f"unknown command {a.command}")


GENDER_WORDS = {"man", "woman", "men", "women", "he", "she", "a", "karl", "kona", "karlar", "konur", "körlum", "konum",
                "hann", "hún", "fjórir", "fjórar", "i'm", "ég", "er", "رجل", "امرأة", "رجال", "نساء",
                "mies", "nainen", "miehestä", "naisesta", "miehistä", "naisista"}


def _is_gender_pair(x, y):
    words = set((x + " " + y).lower().replace(".", " ").replace(",", " ").replace("?", " ").replace("؟", " ").replace("،", " ").split())
    return words <= GENDER_WORDS


if __name__ == "__main__":
    main()
