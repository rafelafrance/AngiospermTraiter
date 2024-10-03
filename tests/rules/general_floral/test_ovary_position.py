import unittest

from angiosperm.pylib.rules.general_floral.ovary_position import OvaryPosition
from tests.setup import general_floral_parse


class TestOvaryPosition(unittest.TestCase):
    def test_ovary_position_01(self):
        self.assertEqual(
            general_floral_parse("Epigynous disk present (large, pulviniform)."),
            [
                OvaryPosition(position="inferior", start=0, end=9),
            ],
        )
