import unittest

from angiosperm.pylib.rules.floral_nectary import FloralNectary
from tests.setup import parse


class TestFloralNectary(unittest.TestCase):
    def test_floral_nectary_01(self):
        self.assertEqual(
            parse("reproductive_type", "floral nectaries present"),
            [
                FloralNectary(present="1", start=0, end=24),
            ],
        )

    def test_floral_nectary_02(self):
        self.assertEqual(
            parse("reproductive_type", "floral nectaries absent"),
            [
                FloralNectary(present="0", start=0, end=23),
            ],
        )
