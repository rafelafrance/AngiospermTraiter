import unittest

from angiosperm.pylib.rules.structural_sex_of_flowers import (
    StructuralSexOfFlowers,
)
from tests.setup import parse


class TestStructuralSexOfFlowers(unittest.TestCase):
    def test_structural_sex_of_flowers_01(self):
        self.assertEqual(
            parse("reproductive_type", "Unisexual flowers present."),
            [StructuralSexOfFlowers(structural_sex="1", start=0, end=25)],
        )
