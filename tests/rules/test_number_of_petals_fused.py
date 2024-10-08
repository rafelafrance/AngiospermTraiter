import unittest

from angiosperm.pylib.rules.number_of_petals_fused import NumberOfPetalsFused
from tests.setup import parse


class TestFlowerCount(unittest.TestCase):
    def test_number_of_petals_fused_01(self):
        self.assertEqual(
            parse("perianth", "petals fused (8–)10(–16)."),
            [NumberOfPetalsFused(min=8, low=10, max=16, start=0, end=24)],
        )

    def test_number_of_petals_fused_02(self):
        self.assertEqual(
            parse("perianth", "8–10 fused petals"),
            [NumberOfPetalsFused(low=8, high=10, start=0, end=17)],
        )
