import unittest

from angiosperm.pylib.rules.androecium.androecium_structural_whorls import (
    NumberOfAndroeciumWhorls,
)
from tests.setup import parse


class TestFlowerCount(unittest.TestCase):
    def test_number_of_perianth_whorls_01(self):
        self.assertEqual(
            parse("androecium", "; 2-whorled."),
            [NumberOfAndroeciumWhorls(low=2, start=2, end=11)],
        )

    def test_number_of_perianth_whorls_02(self):
        self.assertEqual(
            parse("androecium", "; two whorled."),
            [NumberOfAndroeciumWhorls(low=2, start=2, end=13)],
        )

    def test_number_of_perianth_whorls_03(self):
        self.assertEqual(
            parse("androecium", "biseriate"),
            [NumberOfAndroeciumWhorls(low=2, start=0, end=9)],
        )
