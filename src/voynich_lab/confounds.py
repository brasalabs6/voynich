"""Page-level audit of Currier/hand/quire/illustration confounding.

This reports observational overlap/identifiability, not causal effects.
"""
from collections import Counter, defaultdict


def page_table(records) -> list[dict]:
    pages = {}
    for r in records:
        metadata = (r.language or "?", r.hand or "?", r.quire or "?",
                    r.illustration or "?")
        if r.folio not in pages:
            pages[r.folio] = {"id": r.folio, "language": metadata[0],
                              "hand": metadata[1], "quire": metadata[2],
                              "illustration": metadata[3], "tokens": 0, "loci": 0}
        else:
            old = pages[r.folio]
            if (old["language"], old["hand"], old["quire"], old["illustration"]) != metadata:
                raise ValueError("Conflicting page-header metadata on " + r.folio)
        pages[r.folio]["tokens"] += len(r.words)
        pages[r.folio]["loci"] += 1
    return [pages[k] for k in sorted(pages)]


def overlap(pages, keys: tuple[str, ...]) -> dict:
    groups = defaultdict(list)
    for p in pages:
        if p["language"] in ("A", "B") and p["tokens"] > 0:
            groups[tuple(p[key] for key in keys)].append(p)
    matched = {key: ps for key, ps in groups.items()
               if {p["language"] for p in ps} == {"A", "B"}}
    return {
        "stratification": list(keys),
        "n_strata_total": len(groups),
        "n_strata_with_both_A_B": len(matched),
        "matched_folio_sides": sum(len(x) for x in matched.values()),
        "matched_A": sum(p["language"] == "A" for x in matched.values() for p in x),
        "matched_B": sum(p["language"] == "B" for x in matched.values() for p in x),
        "example_matching_strata": [
            {"values": list(key), "A": sum(p["language"] == "A" for p in x),
             "B": sum(p["language"] == "B" for p in x)}
            for key, x in sorted(matched.items())[:30]
        ],
        "warning": "If there is no matched stratum, A/B effect cannot be estimated independent of these covariates."
    }


def audit(records) -> dict:
    pages = page_table(records)
    labels = Counter(p["language"] for p in pages)
    cross = Counter((p["language"], p["hand"]) for p in pages)
    locus_type = Counter((r.locus_type[1:2] or "?") for r in records)
    return {
        "page_sides": len(pages),
        "currier_page_counts": dict(sorted(labels.items())),
        "currier_by_hand_page_counts": [
            {"language": l, "hand": h, "pages": n}
            for (l, h), n in sorted(cross.items())
        ],
        "locus_type_counts": dict(sorted(locus_type.items())),
        "overlap_hand": overlap(pages, ("hand",)),
        "overlap_quire": overlap(pages, ("quire",)),
        "overlap_hand_quire": overlap(pages, ("hand", "quire")),
        "overlap_hand_illustration": overlap(pages, ("hand", "illustration")),
        "status": "descriptive_only_not_a_causal_analyses",
    }

