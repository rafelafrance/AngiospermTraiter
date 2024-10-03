import unittest

from angiosperm.pylib.rules.general_floral.flower_grouping import FlowerGrouping
from tests.setup import general_floral_parse


class TestFlowerGrouping(unittest.TestCase):
    def test_flower_grouping_01(self):
        self.assertEqual(
            general_floral_parse("Flowers aggregated in ‘inflorescences’;"),
            [
                FlowerGrouping(grouping="inflorescence", start=0, end=38),
            ],
        )

    def test_flower_grouping_02(self):
        self.assertEqual(
            general_floral_parse("Flowers usually solitary;"),
            [
                FlowerGrouping(grouping="solitary", start=0, end=25),
            ],
        )

    def test_flower_grouping_03(self):
        self.assertEqual(
            general_floral_parse(
                "Flowers solitary, or aggregated in ‘inflorescences’;"
            ),
            [
                FlowerGrouping(grouping="solitary", start=0, end=17),
                FlowerGrouping(grouping="inflorescence", start=18, end=51),
            ],
        )
