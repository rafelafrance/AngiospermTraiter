import unittest

from angiosperm.pylib.rules.perianth_merism import PerianthMerism
from tests.setup import parse


class TestPerianthMerism(unittest.TestCase):
    def test_perianth_merism_01(self):
        self.assertEqual(
            parse("perianth", "when pentamerous,"),
            [
                PerianthMerism(merism="pentamerous", start=5, end=16),
            ],
        )
