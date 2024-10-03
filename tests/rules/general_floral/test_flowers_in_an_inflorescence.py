import unittest

from angiosperm.pylib.rules.general_floral.flowers_in_an_inflorescence import (
    FlowersInAnInflorescence,
)
from tests.setup import general_floral_parse


class TestFlowerCount(unittest.TestCase):
    def test_flower_count_01(self):
        self.assertEqual(
            general_floral_parse("flowers (8–)10(–16)."),
            [FlowersInAnInflorescence(min=8, low=10, max=16, start=0, end=19)],
        )

    def test_flower_count_02(self):
        self.assertEqual(
            general_floral_parse("8–10–flowered"),
            [FlowersInAnInflorescence(low=8, high=10, start=0, end=13)],
        )
