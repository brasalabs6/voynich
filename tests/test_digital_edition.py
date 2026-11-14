import unittest
from scripts.build_digital_edition import normalize, label

class IndexTests(unittest.TestCase):
    def test_v2(self):
        m={"sequences":[{"canvases":[
          {"@id":"urn:1","label":"1r","images":[{"resource":{"@id":"https://x/full.jpg","service":{"@id":"https://x/iiif/1"}}}]},
          {"@id":"urn:cover","label":"Front cover","images":[{"resource":{"@id":"https://x/cover.jpg"}}]}
        ]}]}
        out=normalize(m,"sha","test")
        self.assertEqual(out["canvas_count"],2)
        self.assertEqual(out["pages"][0]["folio"],"f1r")
        self.assertEqual(out["pages"][0]["image_info"],"https://x/iiif/1/info.json")
        self.assertIsNone(out["pages"][1]["folio"])

    def test_v3(self):
        m={"items":[{"id":"urn:2","type":"Canvas","label":{"en":["Folio 2v"]},
          "items":[{"items":[{"motivation":"painting","body":{
          "id":"https://x/2/full/max/0/default.jpg",
          "service":[{"id":"https://x/iiif/2","type":"ImageService3"}]
          }}]}]}]}
        out=normalize(m,"sha","test")
        self.assertEqual(out["pages"][0]["folio"],"f2v")
        self.assertEqual(out["pages"][0]["image_service"],"https://x/iiif/2")

    def test_duplicates_and_errors(self):
        x=normalize({"items":[{"label":{"none":["f1r"]}},{"label":{"none":["f1r"]}}]},"sha","test")
        self.assertNotEqual(x["pages"][0]["id"], x["pages"][1]["id"])
        with self.assertRaises(ValueError):
            normalize({},"sha","test")
        self.assertEqual(label({"en":["Folio","1r"]}),"Folio 1r")
