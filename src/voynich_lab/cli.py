"""Analyze one versioned IVTFF source and write full provenance."""
import argparse
import hashlib
import json
from pathlib import Path
from .ivtff import load
from .stats import describe, test_line_ending, test_currier


def analyze(path: Path, permutations=199, seed=408) -> dict:
    if permutations < 19:
        raise ValueError("At least 19 permutations required")
    raw = path.read_bytes()
    records = load(str(path))
    return {
        "schema_version": "0.1",
        "status": "EXPLORATORY, NOT A DECIPHERMENT",
        "input": {"filename": path.name, "sha256": hashlib.sha256(raw).hexdigest(),
                  "bytes": len(raw), "format": "IVTFF EVA 2.0"},
        "normalization": "drop ambiguous fragments; dot and comma treated as boundaries",
        "description": describe(records),
        "tests": {
            "H001_currier_ab": test_currier(records, permutations=permutations, seed=seed + 1),
            "H002_line_ending": test_line_ending(records, permutations=permutations, seed=seed),
        },
        "warnings": [
            "EVA is transliteration, not plaintext or a one-to-one manuscript glyph map.",
            "Parser ignores unsupported IVTFF material; review coverage before publication.",
            "Randomization tests are exploratory; uncorrected for multiple comparisons.",
            "Currier test does not disentangle quire, genre or scribal hand.",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["analyze"])
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--permutations", type=int, default=199)
    p.add_argument("--seed", type=int, default=408)
    args = p.parse_args()
    output = analyze(args.input, args.permutations, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Saved", args.output, output["description"]["unambiguous_tokens"], "EVA tokens")


if __name__ == "__main__":
    main()

