import unittest

from angiosperm.pylib.rules.general_floral.floral_nectary_on_perianth import (
    FloralNectaryOnPerianth,
)
from tests.setup import general_floral_parse


class TestFloralNectaryOnPerianth(unittest.TestCase):
    def test_floral_nectary_on_perianth_01(self):
        self.assertEqual(
            general_floral_parse("floral nectary on perianth"),
            [
                FloralNectaryOnPerianth(present=True, start=0, end=26),
            ],
        )
