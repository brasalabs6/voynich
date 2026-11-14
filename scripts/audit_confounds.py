#!/usr/bin/env python3
"""Run a reproducible cross-tabulation and locus-type sensitivity check."""
import argparse
import hashlib
import json
from pathlib import Path

from voynich_lab.ivtff import load
from voynich_lab.confounds import audit
from voynich_lab.stats import test_line_ending


def run(input_path: Path, permutations=199) -> dict:
    records = load(str(input_path))
    result = {
        "schema": "0.1",
        "status": "descriptive_audit_exploratory",
        "input": input_path.name,
        "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "strata": audit(records),
        "line_ending_sensitivity": {},
        "warnings": [
            "Locus types P/L/C/R have different layout semantics.",
            "A/B, hand, quire and illustration are observational variables.",
            "Empty joint overlap makes a conditional A/B effect unidentified.",
            "Unadjusted MC p-values in exploratory tests cannot prove a language.",
        ],
    }
    groups = {
        "all_loci": records,
        "paragraph_P": [r for r in records if r.locus_type[1:2] == "P"],
        "label_L": [r for r in records if r.locus_type[1:2] == "L"],
        "circular_C": [r for r in records if r.locus_type[1:2] == "C"],
        "paragraph_A": [r for r in records if r.locus_type[1:2] == "P" and r.language == "A"],
        "paragraph_B": [r for r in records if r.locus_type[1:2] == "P" and r.language == "B"],
    }
    for name, selection in groups.items():
        valid = sum(len(r.words) >= 3 for r in selection)
        result["line_ending_sensitivity"][name] = {
            "loci": len(selection), "valid_loci": valid,
            "test": test_line_ending(selection, permutations=permutations, seed=408)
            if valid >= 10 else {"status": "insufficient_loci"},
        }
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--permutations", type=int, default=199)
    args = p.parse_args()
    report = run(args.input, args.permutations)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("Wrote", args.output, "A/B hand overlap:", report["strata"]["overlap_hand"]["matched_folio_sides"])

