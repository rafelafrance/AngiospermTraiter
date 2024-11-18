import unittest

from angiosperm.pylib.rules.ovary_position import OvaryPosition
from tests.setup import parse


class TestOvaryPosition(unittest.TestCase):
    def test_ovary_position_01(self):
        self.assertEqual(
            parse("general_floral", "Epigynous disk present (large, pulviniform)."),
            [
                OvaryPosition(position="2", start=0, end=9),
            ],
        )
