import unittest
from scripts.glyph_extract import crop_url

class GlyphCropTests(unittest.TestCase):
    def setUp(self):
        self.page={"image_service":"https://iiif.example.test/2/1","width":300,"height":400}
    def test_valid(self):
        self.assertEqual(crop_url(self.page,{"x":10,"y":20,"w":45,"h":70}),
            "https://iiif.example.test/2/1/10,20,45,70/full/0/default.jpg")
    def test_invalid_bounds(self):
        for r in ({"x":280,"y":20,"w":50,"h":70},
                  {"x":0,"y":0,"w":-1,"h":50},
                  {"x":0,"y":0,"w":True,"h":60}):
            with self.assertRaises(ValueError):
                crop_url(self.page,r)
    def test_no_image_service(self):
        with self.assertRaises(ValueError):
            crop_url({"width":100,"height":100},{"x":0,"y":0,"w":10,"h":10})

