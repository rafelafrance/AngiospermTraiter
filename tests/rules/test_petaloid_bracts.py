import unittest

from angiosperm.pylib.rules.bracts import Bracts
from angiosperm.pylib.rules.petaloid_bracts import PetaloidBracts
from tests.setup import parse


class TestPetaloidBracts(unittest.TestCase):
    def test_petaloid_bract_01(self):
        self.assertEqual(
            parse(
                "general_floral",
                "petaloid ‘bracts’ surpassing the petals",
                append_missing=True,
            ),
            [
                PetaloidBracts(present="1", start=0, end=17),
                Bracts(present="?"),
            ],
        )

    def test_petaloid_bract_02(self):
        self.assertEqual(
            parse(
                "general_floral",
                "without petaloid ‘bracts’ surpassing the petals",
                append_missing=True,
            ),
            [
                PetaloidBracts(present="0", start=0, end=25),
                Bracts(present="?"),
            ],
        )

    def test_petaloid_bract_03(self):
        self.assertEqual(
            parse(
                "general_floral",
                "who knows what's being said",
                append_missing=True,
            ),
            [
                Bracts(present="?"),
                PetaloidBracts(present="?"),
            ],
        )
