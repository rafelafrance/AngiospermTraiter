import unittest

from angiosperm.pylib.rules.perianth.perianth_margin import PerianthMargin
from tests.setup import parse


class TestFloralNectaryOnAndroecium(unittest.TestCase):
    def test_perianth_margin_01(self):
        self.assertEqual(
            parse("perianth", "commonly bilobed or emarginate "),
            [
                PerianthMargin(margin="entire", start=20, end=30),
            ],
        )
