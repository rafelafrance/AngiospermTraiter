import unittest

from angiosperm.pylib.rules.pedicel import Pedicel
from tests.setup import parse


class TestPedicel(unittest.TestCase):
    def test_pedicel_01(self):
        self.assertEqual(
            parse("general_floral", "on slender pedicels"),
            [
                Pedicel(present="1", start=11, end=19),
            ],
        )

    def test_pedicel_02(self):
        self.assertEqual(
            parse("general_floral", "long pedicellate"),
            [
                Pedicel(present="1", start=5, end=16),
            ],
        )

    def test_pedicel_03(self):
        self.assertEqual(
            parse("general_floral", "Sessile"),
            [
                Pedicel(present="0", start=0, end=7),
            ],
        )
