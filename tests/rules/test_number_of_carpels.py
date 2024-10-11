import unittest

from angiosperm.pylib.rules.number_of_carpels import NumberOfCarpels
from tests.setup import parse


class TestFlowerCount(unittest.TestCase):
    def test_number_of_perianth_whorls_01(self):
        self.assertEqual(
            parse("gynoecium", "Gynoecium 1–3–5(–6) carpelled."),
            [NumberOfCarpels(min=1, low=3, high=5, max=6, start=10, end=29)],
        )
