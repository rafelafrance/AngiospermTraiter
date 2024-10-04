import unittest

from angiosperm.pylib.rules.perianth.perianth_differentiation import (
    PerianthDifferentiation,
)
from tests.setup import parse


class TestBract(unittest.TestCase):
    def test_perianth_differentiation_01(self):
        self.assertEqual(
            parse("perianth", "Perianth of tepals"),
            [
                PerianthDifferentiation(
                    differentiation="undifferentiated", start=12, end=18
                ),
            ],
        )
