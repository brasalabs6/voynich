"""Conservative, deliberately incomplete IVTFF 2.0 EVA parser.

The original transcription, with doubts and comments, remains the source of
truth. Transliteration characters do NOT necessarily equal manuscript glyphs.
"""
from dataclasses import dataclass
import re

PAGE = re.compile(r"^<(f\d+[rv]\d*)>\s*(.*)$")
LOCUS = re.compile(r"^<(f\d+[rv]\d*)\.([^,>]+),([^>]+)>\s*(.*)$")
FIELD = re.compile(r"\$([A-Za-z])=([A-Za-z0-9?]+)")
TAGS = re.compile(r"<[^>]*>")
VALID = re.compile(r"[a-z]+")


@dataclass(frozen=True)
class Locus:
    folio: str
    line_id: str
    locus_type: str
    language: str | None
    hand: str | None
    quire: str | None
    illustration: str | None
    raw: str
    words: tuple[str, ...]
    excluded: int


def tokens(raw: str) -> tuple[tuple[str, ...], int]:
    # Both "." and "," treated as boundaries: exploratory choice, not official IVTT.
    fragments = re.split(r"[.,\s]+", TAGS.sub(".", raw))
    kept = tuple(w for w in fragments if VALID.fullmatch(w))
    excluded = sum(bool(w) and not VALID.fullmatch(w) for w in fragments)
    return kept, excluded


def parse(lines) -> list[Locus]:
    metadata: dict[str, dict[str, str]] = {}
    output: list[Locus] = []
    seen = set()
    for source_line in lines:
        line = source_line.strip()
        if not line or line.startswith("#"):
            continue
        m = PAGE.match(line)
        if m:
            metadata[m[1]] = dict(FIELD.findall(m[2]))
            continue
        m = LOCUS.match(line)
        if not m:
            continue
        folio, number, kind, raw = m.groups()
        key = (folio, number, kind)
        if key in seen:
            raise ValueError("Duplicate locus: " + str(key))
        seen.add(key)
        page = metadata.get(folio, {})
        words, excluded = tokens(raw)
        output.append(Locus(folio, number, kind, page.get("L"), page.get("H"),
                            page.get("Q"), page.get("I"), raw, words, excluded))
    if not output:
        raise ValueError("No locus records found; verify IVTFF source")
    return output


def load(path: str) -> list[Locus]:
    with open(path, encoding="utf-8-sig") as handle:
        return parse(handle)

