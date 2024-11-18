import unittest

from angiosperm.pylib.rules.plant_sexual_system import (
    PlantSexualSystem,
)
from tests.setup import parse


class TestSexualSystem(unittest.TestCase):
    def test_sexual_system_01(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                "reproductive_type",
                "Plants monoecious, or dioecious, or polygamomonoecious (?).",
            ),
            [
                PlantSexualSystem(sexual_system="0", start=7, end=17),
                PlantSexualSystem(sexual_system="1", start=22, end=31),
                PlantSexualSystem(sexual_system="polygamomonoecious", start=36, end=54),
            ],
        )
