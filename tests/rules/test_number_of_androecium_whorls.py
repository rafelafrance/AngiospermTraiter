import unittest

from angiosperm.pylib.rules.androecium_structural_whorls import NumberOfAndroeciumWhorls
from tests.setup import parse


class TestNumberOfAndroeciumWhorls(unittest.TestCase):
    def test_androecium_structural_whorls_01(self):
        self.assertEqual(
            parse("androecium", "; 2-whorled."),
            [NumberOfAndroeciumWhorls(low=2, start=2, end=11)],
        )

    def test_androecium_structural_whorls_02(self):
        self.assertEqual(
            parse("androecium", "; two whorled."),
            [NumberOfAndroeciumWhorls(low=2, start=2, end=13)],
        )

    def test_androecium_structural_whorls_03(self):
        self.assertEqual(
            parse("androecium", "biseriate"),
            [NumberOfAndroeciumWhorls(low=2, start=0, end=9)],
        )
