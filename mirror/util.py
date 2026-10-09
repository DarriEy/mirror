"""Shared helpers: config, paths, hashing, JSON I/O."""
import hashlib
import json
import os
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_config(path):
    with open(path, "rb") as f:
        cfg = tomllib.load(f)
    cfg["_path"] = str(Path(path).resolve())
    study = cfg.setdefault("study", {})
    study.setdefault("name", "mirror")
    study.setdefault("languages", ["en"])
    study.setdefault("seed", 20261003)
    study.setdefault("reps_S", 10)
    study.setdefault("reps_F", 4)
    study.setdefault("gender_check", True)
    study.setdefault("max_output_tokens", 2048)
    study.setdefault("concurrency", 4)
    study.setdefault("out_dir", "studies")
    cfg.setdefault("models", [])
    cfg.setdefault("rating", {}).setdefault("raters", [])
    cfg["rating"].setdefault("batch_size", 12)
    cfg["rating"].setdefault("human_sample_fraction", 0.2)
    a = cfg.setdefault("analysis", {})
    a.setdefault("equivalence_raise", 0.10)
    a.setdefault("equivalence_likelihood", 10.0)
    a.setdefault("equivalence_net_legitimacy", 0.5)
    a.setdefault("bootstrap", 5000)
    a.setdefault("permutations", 10000)
    return cfg


def study_dir(cfg):
    base = Path(cfg["study"]["out_dir"])
    if not base.is_absolute():
        base = Path(cfg["_path"]).parent / base
    d = base / cfg["study"]["name"]
    d.mkdir(parents=True, exist_ok=True)
    return d


def slug(model_id):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model_id)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_jsonl(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def scenario_file(lang):
    return ROOT / "scenarios" / f"{lang}.json"


def api_key(model_cfg):
    env = model_cfg.get("key_env")
    if not env:
        return None
    key = os.environ.get(env)
    if not key:
        raise SystemExit(f"Missing API key: set the environment variable {env}")
    return key
