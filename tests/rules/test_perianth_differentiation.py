import unittest

from angiosperm.pylib.rules.perianth_differentiation import PerianthDifferentiation
from tests.setup import parse


class TestPerianthDifferentiation(unittest.TestCase):
    def test_perianth_differentiation_01(self):
        self.assertEqual(
            parse("perianth", "Perianth of tepals"),
            [
                PerianthDifferentiation(differentiation="0", start=0, end=18),
            ],
        )
