"""Descriptive A/B contrast in suffix location, with cluster bootstrap CIs.

WARNING: These intervals quantify sample variability under two resampling
schemes. Because A/B strongly confounds hand/quire, they are NOT causal
evidence of two languages or a decipherment.
"""
from collections import defaultdict
import random


def sample_rows(records, suffix="dy") -> list[dict]:
    per_page = {}
    for r in records:
        if r.language not in {"A", "B"} or r.locus_type[1:2] != "P" or len(r.words) < 3:
            continue
        k = r.folio
        if k not in per_page:
            per_page[k] = {
                "page": k, "language": r.language, "hand": r.hand or "?",
                "quire": r.quire or "?", "loci": 0,
                "end_hits": 0, "end_total": 0, "mid_hits": 0, "mid_total": 0,
            }
        p = per_page[k]
        if p["language"] != r.language:
            raise ValueError("Conflicting A/B on " + k)
        p["loci"] += 1
        p["end_total"] += 1
        p["end_hits"] += int(r.words[-1].endswith(suffix))
        p["mid_total"] += len(r.words) - 2
        p["mid_hits"] += sum(w.endswith(suffix) for w in r.words[1:-1])
    return [per_page[k] for k in sorted(per_page)]


def score(rows: list[dict]) -> float | None:
    end_n = sum(p["end_total"] for p in rows)
    mid_n = sum(p["mid_total"] for p in rows)
    if not end_n or not mid_n:
        return None
    return sum(p["end_hits"] for p in rows) / end_n - sum(p["mid_hits"] for p in rows) / mid_n


def contrast(rows: list[dict]) -> float | None:
    a = score([x for x in rows if x["language"] == "A"])
    b = score([x for x in rows if x["language"] == "B"])
    return None if a is None or b is None else b - a


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    idx = (len(ordered) - 1) * q
    lower = int(idx)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] * (upper - idx) + ordered[upper] * (idx - lower) if lower != upper else ordered[lower]


def bootstrap(records, suffix="dy", repetitions=999, seed=408) -> dict:
    if repetitions < 30:
        raise ValueError("At least 30 bootstrap samples recommended")
    rows = sample_rows(records, suffix=suffix)
    a, b = ([p for p in rows if p["language"] == label] for label in ("A", "B"))
    observed = contrast(rows)
    if observed is None:
        return {"status": "insufficient_A_B_coverage"}
    rng = random.Random(seed)
    page_values, quire_values = [], []
    for _ in range(repetitions):
        # Each page-side is sampled within A/B; this is optimistic if neighboring
        # pages share unmodeled quire effects.
        page_draw = ([rng.choice(a) for _ in a] + [rng.choice(b) for _ in b])
        page_values.append(contrast(page_draw))
    by_quire = defaultdict(list)
    for p in rows:
        by_quire[p["quire"]].append(p)
    quires = sorted(by_quire)
    for _ in range(repetitions):
        # Resample entire quires preserving their internal page and A/B structure.
        draw = [p for q in [rng.choice(quires) for _ in quires] for p in by_quire[q]]
        c = contrast(draw)
        if c is not None:
            quire_values.append(c)
    def summarise(values):
        return {
            "n_successful": len(values),
            "percentile_95_ci": [round(percentile(values, .025), 8), round(percentile(values, .975), 8)] if values else None,
            "fraction_negative": round(sum(v < 0 for v in values) / len(values), 6) if values else None,
        }
    return {
        "status": "exploratory_noncausal",
        "suffix": suffix, "end_minus_middle_A": round(score(a), 8),
        "end_minus_middle_B": round(score(b), 8),
        "B_minus_A": round(observed, 8),
        "n_A_pages": len(a), "n_B_pages": len(b),
        "n_A_loci": sum(p["loci"] for p in a), "n_B_loci": sum(p["loci"] for p in b),
        "n_unique_quires": len(quires),
        "bootstrap_pages": summarise(page_values),
        "bootstrap_quires": summarise(quire_values),
        "repetitions": repetitions, "seed": seed,
        "limitations": [
            "No random assignment of Currier labels; overlap hand×quire absent in baseline.",
            "Page bootstrap underestimates uncertainty if within-quire correlation is strong.",
            "Quire bootstrap approximates dependence but cannot identify an A/B causal contrast.",
            "EVA/IVTFF segmentation may induce edge effects; varying label/space policy is future work.",
        ],
    }

