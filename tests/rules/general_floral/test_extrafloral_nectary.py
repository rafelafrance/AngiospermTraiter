import unittest

from angiosperm.pylib.rules.general_floral.extrafloral_nectary import (
    ExtrafloralNectary,
)
from tests.setup import parse


class TestExtrafloralNectary(unittest.TestCase):
    def test_extrafloral_nectary_01(self):
        self.assertEqual(
            parse(
                "general_floral", "often with a pair of glands or extrafloral nectaries"
            ),
            [
                ExtrafloralNectary(present=True, start=31, end=52),
            ],
        )