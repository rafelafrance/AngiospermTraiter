import unittest

from angiosperm.pylib.rules.structural_sex import StructuralSex
from tests.setup import parse


class TestStructuralSexOfFlowers(unittest.TestCase):
    def test_structural_sex_of_flowers_01(self):
        self.assertEqual(
            parse("Unisexual flowers present."),
            [
                StructuralSex(structural_sex="unisexual", start=0, end=9),
            ],
        )
