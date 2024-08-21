import unittest

from angiosperm.pylib.rules.flower_count import FlowerCount
from tests.setup import parse


class TestFlowerCount(unittest.TestCase):
    def test_flower_count_01(self):
        self.assertEqual(
            parse("flowers (8–)10(–16)."),
            [FlowerCount(min=8, low=10, max=16, start=0, end=19)],
        )

    def test_flower_count_02(self):
        self.assertEqual(
            parse("8–10–flowered"),
            [FlowerCount(low=8, high=10, start=0, end=13)],
        )
