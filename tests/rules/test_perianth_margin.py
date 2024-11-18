import unittest

from angiosperm.pylib.rules.perianth_margin import PerianthMargin
from tests.setup import parse


class TestPerianthMargin(unittest.TestCase):
    def test_perianth_margin_01(self):
        self.assertEqual(
            parse("perianth", "commonly bilobed or emarginate "),
            [
                PerianthMargin(margin="0", start=20, end=30),
            ],
        )
