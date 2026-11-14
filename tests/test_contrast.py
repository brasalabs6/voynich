import unittest
from voynich_lab.ivtff import parse
from voynich_lab.contrast import bootstrap, percentile, sample_rows, contrast, score

class ContrastTests(unittest.TestCase):
    def test_simple_difference(self):
        records = parse([
            "<f1r> <! $Q=A $L=A $H=1>",
            "<f1r.1,@P0> ol.chol.shedy",
            "<f2r> <! $Q=B $L=B $H=2>",
            "<f2r.1,@P0> shedy.ol.chol",
        ])
        self.assertEqual(bootstrap(records, repetitions=99, seed=1)["B_minus_A"], -1.0)
        self.assertEqual(bootstrap(records, repetitions=99, seed=1),
                         bootstrap(records, repetitions=99, seed=1))
        self.assertEqual(percentile([1,2,3,4], .5), 2.5)

    def test_empty(self):
        self.assertEqual(score([]), None)

if __name__ == "__main__":
    unittest.main()

