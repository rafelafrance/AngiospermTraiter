import unittest

from angiosperm.pylib.rules.number_of_whorls import NumberOfWhorls
from tests.setup import parse


class TestNumberOfAndroeciumWhorls(unittest.TestCase):
    def test_androecium_structural_whorls_01(self):
        self.assertEqual(
            parse("androecium", "; 2-whorled."),
            [
                NumberOfWhorls(
                    _trait="number_of_androecium_whorls", low=2, start=2, end=11
                )
            ],
        )

    def test_androecium_structural_whorls_02(self):
        self.assertEqual(
            parse("androecium", "; two whorled."),
            [
                NumberOfWhorls(
                    _trait="number_of_androecium_whorls", low=2, start=2, end=13
                )
            ],
        )

    def test_androecium_structural_whorls_03(self):
        self.assertEqual(
            parse("androecium", "biseriate"),
            [
                NumberOfWhorls(
                    _trait="number_of_androecium_whorls",
                    low=2,
                    start=0,
                    end=9,
                )
            ],
        )
