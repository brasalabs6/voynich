import unittest
from voynich_lab.ivtff import parse

class RosetteLocusTests(unittest.TestCase):
    def test_special_fRos_folio(self):
        records = parse([
            "<fRos> <! $Q=N $L=B $H=4>",
            "<fRos.1,@L0> <!1:11>saeeasa?",
            "<fRos.2,@Cc> <!10:30>oto.tosaes.adar",
        ])
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].folio, "fRos")
        self.assertEqual(records[0].language, "B")
        self.assertEqual(records[1].words, ("oto", "tosaes", "adar"))

if __name__ == "__main__":
    unittest.main()
