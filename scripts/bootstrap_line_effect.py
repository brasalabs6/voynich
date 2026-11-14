#!/usr/bin/env python3
"""Run cluster-robust exploratory A/B line suffix contrast for IVTFF."""
import argparse
import hashlib
import json
from pathlib import Path
from voynich_lab.ivtff import load
from voynich_lab.contrast import bootstrap

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=999)
    parser.add_argument("--seed", type=int, default=408)
    args = parser.parse_args()
    result = {
        "schema":"0.1", "status":"exploratory_not_a_translation",
        "source": args.input.name,
        "source_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "model": bootstrap(load(str(args.input)), repetitions=args.repetitions, seed=args.seed),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Wrote",args.output,"B-A",result["model"].get("B_minus_A"))

