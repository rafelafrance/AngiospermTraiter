import unittest

from angiosperm.pylib.rules.general_floral.petaloid_bracts import (
    PetaloidBracts,
)
from tests.setup import parse


class TestPetaloidBracts(unittest.TestCase):
    def test_petaloid_bract_01(self):
        self.assertEqual(
            parse("general_floral", "petaloid ‘bracts’ surpassing the petals"),
            [
                PetaloidBracts(present=True, start=0, end=17),
            ],
        )

    def test_petaloid_bract_02(self):
        self.assertEqual(
            parse("general_floral", "without petaloid ‘bracts’ surpassing the petals"),
            [
                PetaloidBracts(present=False, start=0, end=25),
            ],
        )
