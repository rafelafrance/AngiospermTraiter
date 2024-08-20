import unittest

from angiosperm.pylib.rules.flower_grouping import FlowerGrouping
from tests.setup import parse


class TestSexualSystem(unittest.TestCase):
    def test_flower_grouping_01(self):
        self.assertEqual(
            parse("Flowers aggregated in ‘inflorescences’;"),
            [
                FlowerGrouping(flower_grouping="inflorescence", start=0, end=38),
            ],
        )

    def test_flower_grouping_02(self):
        self.assertEqual(
            parse("Flowers usually solitary;"),
            [
                FlowerGrouping(flower_grouping="solitary", start=0, end=25),
            ],
        )

    def test_flower_grouping_03(self):
        self.assertEqual(
            parse("Flowers solitary, or aggregated in ‘inflorescences’;"),
            [
                FlowerGrouping(flower_grouping="solitary", start=0, end=17),
                FlowerGrouping(flower_grouping="inflorescence", start=18, end=51),
            ],
        )
