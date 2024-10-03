import unittest

from angiosperm.pylib.rules.general_floral.floral_nectary_on_gynoecium import (
    FloralNectaryOnGynoecium,
)
from tests.setup import general_floral_parse


class TestBract(unittest.TestCase):
    def test_bract_01(self):
        self.assertEqual(
            general_floral_parse("floral nectaries on gynoecium"),
            [
                FloralNectaryOnGynoecium(present=True, start=0, end=29),
            ],
        )
