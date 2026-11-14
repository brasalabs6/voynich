"""Descriptive statistics and page/line-aware permutation nulls."""
from collections import Counter, defaultdict
import math
import random


def entropy(counts: Counter) -> float:
    total = sum(counts.values())
    return -sum((v / total) * math.log2(v / total) for v in counts.values() if v) if total else 0.0


def js_divergence(a: Counter, b: Counter) -> float:
    na, nb = sum(a.values()), sum(b.values())
    if not na or not nb:
        return 0.0
    result = 0.0
    for key in a.keys() | b.keys():
        p, q = a[key] / na, b[key] / nb
        mix = (p + q) / 2
        if p:
            result += p * math.log2(p / mix) / 2
        if q:
            result += q * math.log2(q / mix) / 2
    return result


def describe(records) -> dict:
    all_words = [word for line in records for word in line.words]
    counts = Counter(all_words)
    chars = Counter("".join(all_words))
    by_language, by_hand = Counter(), Counter()
    for rec in records:
        by_language[rec.language or "unknown"] += len(rec.words)
        by_hand[rec.hand or "unknown"] += len(rec.words)
    return {
        "loci": len(records),
        "folio_sides": len({r.folio for r in records}),
        "unambiguous_tokens": len(all_words),
        "excluded_uncertain_fragments": sum(r.excluded for r in records),
        "types": len(counts),
        "hapax_types": sum(n == 1 for n in counts.values()),
        "type_token_ratio": round(len(counts) / len(all_words), 6) if all_words else 0,
        "mean_eva_length": round(sum(map(len, all_words)) / len(all_words), 4) if all_words else 0,
        "eva_char_entropy_bits": round(entropy(chars), 6),
        "top_20": counts.most_common(20),
        "by_currier_label": dict(sorted(by_language.items())),
        "by_scribal_hand": dict(sorted(by_hand.items())),
    }


def test_line_ending(records, suffix="dy", permutations=199, seed=408) -> dict:
    lines = [list(r.words) for r in records if len(r.words) >= 3]
    def metric(rows):
        end = sum(row[-1].endswith(suffix) for row in rows)
        mid = sum(w.endswith(suffix) for row in rows for w in row[1:-1])
        mid_n = sum(len(row) - 2 for row in rows)
        return end / len(rows) - mid / mid_n if rows and mid_n else 0.0
    observed = metric(lines)
    rng = random.Random(seed)
    sample = []
    for _ in range(permutations):
        shuffled = [rng.sample(row, len(row)) for row in lines]
        sample.append(metric(shuffled))
    center = sum(sample) / len(sample)
    p = (1 + sum(abs(v - center) >= abs(observed - center) for v in sample)) / (1 + len(sample))
    return {
        "test": "within-locus shuffle: suffix dy at end versus middle",
        "valid_loci": len(lines), "observed": round(observed, 8),
        "null_mean": round(center, 8), "p_two_sided": round(p, 6),
        "permutations": permutations, "seed": seed,
        "status": "exploratory_not_a_translation",
    }


def test_currier(records, permutations=199, seed=409) -> dict:
    # Permutation unit: page side; not token. Confounding remains by quire/hand.
    page_counts = defaultdict(Counter)
    label = {}
    for rec in records:
        if rec.language not in ("A", "B"):
            continue
        if rec.folio in label and label[rec.folio] != rec.language:
            raise ValueError("Conflicting Currier label on " + rec.folio)
        label[rec.folio] = rec.language
        page_counts[rec.folio].update(word[-2:] for word in rec.words)
    pages = sorted(p for p in page_counts if page_counts[p])
    labels = [label[p] for p in pages]
    if not all(x in labels for x in ("A", "B")):
        return {"status": "insufficient_A_B_coverage"}
    def metric(labs):
        groups = {"A": Counter(), "B": Counter()}
        for page, lab in zip(pages, labs):
            groups[lab].update(page_counts[page])
        return js_divergence(groups["A"], groups["B"])
    obs = metric(labels)
    rng = random.Random(seed)
    vals = []
    for _ in range(permutations):
        perm = labels.copy()
        rng.shuffle(perm)
        vals.append(metric(perm))
    p = (1 + sum(v >= obs for v in vals)) / (1 + len(vals))
    return {
        "test": "Currier A/B suffix-2 Jensen-Shannon divergence, permuted folio sides",
        "observed_js_bits": round(obs, 8),
        "null_mean": round(sum(vals) / len(vals), 8),
        "p_right_tail": round(p, 6),
        "A_folio_sides": labels.count("A"), "B_folio_sides": labels.count("B"),
        "permutations": permutations, "seed": seed,
        "status": "exploratory_cannot_establish_two_languages",
    }

