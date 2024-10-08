import unittest

from angiosperm.pylib.rules.extrafloral_nectary import (
    ExtrafloralNectary,
)
from tests.setup import parse


class TestExtrafloralNectary(unittest.TestCase):
    def test_extrafloral_nectary_01(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                "often with a pair of glands or extrafloral nectaries",
            ),
            [
                ExtrafloralNectary(present=True, start=31, end=52),
            ],
        )

    def test_extrafloral_nectary_02(self):
        self.assertEqual(
            parse("leaf", "or extrafloral nectaries at the base of the blade"),
            [
                ExtrafloralNectary(present=True, start=3, end=24),
            ],
        )
