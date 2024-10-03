import unittest

from angiosperm.pylib.rules.general_floral.structural_sex_of_flowers import (
    StructuralSexOfFlowers,
)
from tests.setup import general_floral_parse


class TestStructuralSexOfFlowers(unittest.TestCase):
    def test_structural_sex_of_flowers_01(self):
        self.maxDiff = None
        self.assertEqual(
            general_floral_parse("Unisexual flowers present."),
            [
                StructuralSexOfFlowers(structural_sex="unisexual", start=0, end=9),
            ],
        )
