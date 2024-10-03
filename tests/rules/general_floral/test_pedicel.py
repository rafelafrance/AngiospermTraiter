import unittest

from angiosperm.pylib.rules.general_floral.pedicel import Pedicel
from tests.setup import general_floral_parse


class TestPetaloidBracts(unittest.TestCase):
    def test_pedicel_01(self):
        self.assertEqual(
            general_floral_parse("on slender pedicels"),
            [
                Pedicel(present=True, start=11, end=19),
            ],
        )

    def test_pedicel_02(self):
        self.assertEqual(
            general_floral_parse("long pedicellate"),
            [
                Pedicel(present=True, start=5, end=16),
            ],
        )
