import unittest

from angiosperm.pylib.rules.floral_nectary_on_gynoecium import (
    FloralNectaryOnGynoecium,
)
from tests.setup import parse


class TestBract(unittest.TestCase):
    def test_bract_01(self):
        self.assertEqual(
            parse("reproductive_type", "floral nectaries on gynoecium"),
            [
                FloralNectaryOnGynoecium(present=True, start=0, end=29),
            ],
        )
