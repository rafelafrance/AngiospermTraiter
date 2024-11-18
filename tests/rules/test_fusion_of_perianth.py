import unittest

from angiosperm.pylib.rules.fusion_of_perianth import FusionOfPerianth
from tests.setup import parse


class TestFusionOfPerianth(unittest.TestCase):
    def test_fusion_of_perianth_01(self):
        self.assertEqual(
            parse("perianth", "basally connate,"),
            [
                FusionOfPerianth(fusion="2", start=0, end=15),
            ],
        )
