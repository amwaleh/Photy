from main.effects import *
from django.test import TestCase
from PIL import Image
from sample_image import TEST_IMAGE
import StringIO


class TestEffects(TestCase):
    """Test Image effects."""

    def setUp(self):
        """Setup image and effect."""
        self.image = Image.open(StringIO.StringIO(TEST_IMAGE))
        self.effect = effect

    def test_effects(self):
        """Test Effects applied on an image."""
        for effect in self.effect:
            image = self.effect[effect](self.image)
            im = type(image).__name__
            self.assertGreater(im.rfind("Image"), -1)
