import unittest
from collections import Counter
from voynich_lab.ivtff import parse, tokens
from voynich_lab.stats import describe, entropy, js_divergence, test_line_ending, test_currier


class LabTests(unittest.TestCase):
    def setUp(self):
        self.lines = parse([
            "#=IVTFF Eva- 2.0 M 5",
            "<f1r> <! $Q=A $L=A $H=1>",
            "<f1r.1,@P0> <%>chol.daiin.qokedy",
            "<f1r.2,+P0> chol.shedy.qokedy",
            "<f2r> <! $Q=B $L=B $H=2>",
            "<f2r.1,@P0> qokedy.qokedy.chol",
            "<f2r.2,+P0> qokedy.chol.shedy",
        ])

    def test_ambiguity(self):
        self.assertEqual(tokens("daiin.ok[a:o]in.???<->chol,shol<$>"),
                         (("daiin", "chol", "shol"), 2))

    def test_metadata(self):
        self.assertEqual(self.lines[0].language, "A")
        self.assertEqual(self.lines[-1].hand, "2")
        self.assertEqual(len(self.lines), 4)
        self.assertEqual(describe(self.lines)["unambiguous_tokens"], 12)

    def test_statistics(self):
        self.assertAlmostEqual(entropy(Counter("abba")), 1)
        self.assertAlmostEqual(js_divergence(Counter(a=1), Counter(b=1)), 1)
        self.assertAlmostEqual(js_divergence(Counter(a=1), Counter(a=3)), 0)

    def test_permutation_determinism(self):
        x = test_line_ending(self.lines, permutations=19, seed=1)
        self.assertEqual(x, test_line_ending(self.lines, permutations=19, seed=1))
        self.assertGreaterEqual(x["p_two_sided"], 0.05)
        self.assertIn("observed_js_bits", test_currier(self.lines, permutations=19))

    def test_reject_duplicates_and_empty(self):
        with self.assertRaises(ValueError):
            parse(["<f1r.1,@P0> abc", "<f1r.1,@P0> abc"])
        with self.assertRaises(ValueError):
            parse(["# none"])


if __name__ == "__main__":
    unittest.main()

