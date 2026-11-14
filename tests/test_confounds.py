import unittest
from voynich_lab.confounds import audit
from voynich_lab.ivtff import parse


class ConfoundsTests(unittest.TestCase):
    def test_non_identifiability_no_overlapping_hands(self):
        records = parse([
            "<f1r> <! $Q=A $L=A $H=1 $I=H>",
            "<f1r.1,@P0> chey.daiin.chol",
            "<f1v> <! $Q=A $L=A $H=1 $I=H>",
            "<f1v.1,@P0> chey.daiin.chol",
            "<f2r> <! $Q=B $L=B $H=2 $I=T>",
            "<f2r.1,@P0> qokedy.shedy.qokeey",
        ])
        result = audit(records)
        self.assertEqual(result["overlap_hand"]["matched_folio_sides"], 0)
        self.assertEqual(result["currier_page_counts"], {"A": 2, "B": 1})

    def test_overlapping_hands_but_not_quires(self):
        records = parse([
            "<f1r> <! $Q=A $L=A $H=1>",
            "<f1r.1,@P0> chey.daiin.chol",
            "<f2r> <! $Q=B $L=B $H=1>",
            "<f2r.1,@P0> qokedy.shedy.qokeey",
        ])
        result = audit(records)
        self.assertEqual(result["overlap_hand"]["matched_folio_sides"], 2)
        self.assertEqual(result["overlap_hand_quire"]["matched_folio_sides"], 0)


if __name__ == "__main__":
    unittest.main()

