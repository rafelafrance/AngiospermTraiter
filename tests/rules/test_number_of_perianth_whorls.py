import unittest

from angiosperm.pylib.rules.number_of_whorls import NumberOfWhorls
from tests.setup import parse


class TestNumberOfWhorls(unittest.TestCase):
    def test_number_of_perianth_whorls_01(self):
        self.assertEqual(
            parse("perianth", "; 2-whorled."),
            [NumberOfWhorls(low=2, start=2, end=11)],
        )

    def test_number_of_perianth_whorls_02(self):
        self.assertEqual(
            parse("perianth", "; two whorled."),
            [NumberOfWhorls(low=2, start=2, end=13)],
        )

    def test_number_of_perianth_whorls_03(self):
        self.assertEqual(
            parse("perianth", "the abaxially pilose lobes biseriate"),
            [NumberOfWhorls(low=2, start=27, end=36)],
        )
