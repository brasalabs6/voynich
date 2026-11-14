"""Offline contract tests for IIIF crop extraction (Issue #8).
Run: python -m unittest discover -s tests -p 'test_glyph_extract_contract.py' -v
No live Yale requests, no fabricated glyphs.
"""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from glyph_extract import crop_url, run

PAGE = {"id": "f1r", "folio": "f1r", "canvas": "https://example.org/canvas/1",
        "image_service": "https://example.org/iiif/1", "width": 100, "height": 200}
SAMPLE = {"id": "GLYPH-SPECIMEN-0001", "page_id": "f1r", "line_id": "f1r.1",
          "x": 90, "y": 190, "w": 10, "h": 10, "candidate": "unknown", "reviewers": []}


class CropContract(unittest.TestCase):
    def test_exact_boundary_and_url(self):
        self.assertEqual(crop_url(PAGE, SAMPLE),
                         "https://example.org/iiif/1/90,190,10,10/full/0/default.jpg")

    def test_invalid_rectangles_and_types(self):
        for change in ({"x": -1}, {"w": 0}, {"x": 91}, {"y": 191},
                       {"w": True}, {"h": 1.5}, {"x": "90"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                crop_url(PAGE, {**SAMPLE, **change})

    def test_missing_service(self):
        with self.assertRaises(ValueError):
            crop_url({**PAGE, "image_service": None}, SAMPLE)

    def test_dry_run_records_unreviewed_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            index, annotations, output = base / "index.json", base / "samples.json", base / "out"
            index.write_text(json.dumps({"source_sha256": "abc123", "pages": [PAGE]}))
            annotations.write_text(json.dumps({"specimens": [SAMPLE]}))
            run(index, annotations, output, dry_run=True)
            specimen = json.loads((output / "glyph-crops-manifest.json").read_text())["specimens"][0]
            self.assertEqual(specimen["status"], "unreviewed_sample")
            self.assertEqual(specimen["source_index_sha256"], "abc123")
            self.assertEqual(specimen["source_canvas"], PAGE["canvas"])
            self.assertEqual(specimen["region_px"], {k: SAMPLE[k] for k in ("x", "y", "w", "h")})
            self.assertNotIn("sha256", specimen)
            self.assertEqual(list(output.glob("*.jpg")), [])

    def test_duplicate_id_fails_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            index, annotations = base / "index.json", base / "samples.json"
            index.write_text(json.dumps({"source_sha256": "abc123", "pages": [PAGE]}))
            annotations.write_text(json.dumps({"specimens": [SAMPLE, SAMPLE]}))
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                run(index, annotations, base / "out", dry_run=True)

    def test_invalid_jpeg_does_not_create_specimen(self):
        class FakeResponse:
            def __enter__(self): return self
            def __exit__(self, *args): return None
            def read(self): return b"not a jpeg" * 20
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            index, annotations, output = base / "index.json", base / "samples.json", base / "out"
            index.write_text(json.dumps({"source_sha256": "abc123", "pages": [PAGE]}))
            annotations.write_text(json.dumps({"specimens": [SAMPLE]}))
            with patch("glyph_extract.urllib.request.urlopen", return_value=FakeResponse()):
                with self.assertRaisesRegex(ValueError, "not a valid JPEG"):
                    run(index, annotations, output)
            self.assertEqual(list(output.glob("*.jpg")), [])


if __name__ == "__main__":
    unittest.main()
