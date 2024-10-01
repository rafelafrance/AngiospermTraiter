import unittest

from angiosperm.pylib.rules.structural_sex_of_flowers import StructuralSexOfFlowers
from tests.setup import parse


class TestStructuralSexOfFlowers(unittest.TestCase):
    def test_structural_sex_of_flowers_01(self):
        self.maxDiff = None
        self.assertEqual(
            parse("Unisexual flowers present."),
            [
                StructuralSexOfFlowers(structural_sex="unisexual", start=0, end=9),
            ],
        )
