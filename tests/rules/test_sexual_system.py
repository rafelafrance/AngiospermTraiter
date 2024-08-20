import unittest

from angiosperm.pylib.rules.sexual_system import SexualSystem
from tests.setup import parse


class TestSexualSystem(unittest.TestCase):
    def test_sexual_system_01(self):
        self.assertEqual(
            parse("Plants monoecious, or dioecious, or polygamomonoecious (?)."),
            [
                SexualSystem(sexual_system="monoecy", start=7, end=17),
                SexualSystem(sexual_system="dioecy", start=22, end=31),
                SexualSystem(
                    sexual_system="polygamomonoecy", uncertain=True, start=36, end=58
                ),
            ],
        )
