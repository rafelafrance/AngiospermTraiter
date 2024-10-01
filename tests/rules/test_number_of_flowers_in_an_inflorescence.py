import unittest

from angiosperm.pylib.rules.number_of_flowers_in_an_inflorescence import (
    NumberOfFlowersInAnInflorescence,
)
from tests.setup import parse


class TestFlowerCount(unittest.TestCase):
    def test_flower_count_01(self):
        self.assertEqual(
            parse("flowers (8–)10(–16)."),
            [NumberOfFlowersInAnInflorescence(min=8, low=10, max=16, start=0, end=19)],
        )

    def test_flower_count_02(self):
        self.assertEqual(
            parse("8–10–flowered"),
            [NumberOfFlowersInAnInflorescence(low=8, high=10, start=0, end=13)],
        )
