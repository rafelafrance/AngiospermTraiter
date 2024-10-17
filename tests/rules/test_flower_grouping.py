import unittest

from angiosperm.pylib.rules.flower_grouping import FlowerGrouping
from tests.setup import parse


class TestFlowerGrouping(unittest.TestCase):
    def test_flower_grouping_01(self):
        self.assertEqual(
            parse("general_floral", "Flowers aggregated in ‘inflorescences’;"),
            [
                FlowerGrouping(grouping="1", start=0, end=38),
            ],
        )

    def test_flower_grouping_02(self):
        self.assertEqual(
            parse("general_floral", "Flowers usually solitary;"),
            [
                FlowerGrouping(grouping="0", start=0, end=24),
            ],
        )

    def test_flower_grouping_03(self):
        self.assertEqual(
            parse(
                "general_floral", "Flowers solitary, or aggregated in ‘inflorescences’;"
            ),
            [
                FlowerGrouping(grouping="0", start=0, end=16),
                FlowerGrouping(grouping="1", start=21, end=51),
            ],
        )
