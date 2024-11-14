import unittest

from angiosperm.pylib.rules.nectar_secretion import NectarSecretion
from tests.setup import parse


class TestNectarSecretion(unittest.TestCase):
    def test_nectar_secretion_01(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                "Nectar secretion from the gynoecium (via septal nectaries).",
            ),
            [
                NectarSecretion(organs=["gynoecium"], start=0, end=35),
            ],
        )

    def test_nectar_secretion_02(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                "Nectar secretion from the perianth, or from the androecium",
            ),
            [
                NectarSecretion(organs=["androecium", "perianth"], start=0, end=58),
            ],
        )

    def test_nectar_secretion_03(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                "Nectar secretion from the perianth (from the tepal bases).",
            ),
            [
                NectarSecretion(organs=["perianth"], start=0, end=34),
            ],
        )
