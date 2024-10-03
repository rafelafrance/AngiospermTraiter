import unittest

from angiosperm.pylib.rules.general_floral.plant_sexual_system import PlantSexualSystem
from tests.setup import general_floral_parse


class TestSexualSystem(unittest.TestCase):
    def test_sexual_system_01(self):
        self.maxDiff = None
        self.assertEqual(
            general_floral_parse(
                "Plants monoecious, or dioecious, or polygamomonoecious (?)."
            ),
            [
                PlantSexualSystem(sexual_system="monoecy", start=7, end=17),
                PlantSexualSystem(sexual_system="dioecy", start=22, end=31),
                PlantSexualSystem(
                    sexual_system="polygamomonoecy", uncertain=True, start=36, end=58
                ),
            ],
        )
