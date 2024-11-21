import unittest

from angiosperm.pylib.rules.floral_nectary import FloralNectary
from angiosperm.pylib.rules.nectar_secretion import NectarSecretion
from angiosperm.pylib.rules.nectaries_secretion import (
    FloralNectaryOnAndroecium,
    FloralNectaryOnGynoecium,
    FloralNectaryOnPerianth,
)
from tests.setup import parse


class TestNectarSecretion(unittest.TestCase):
    def test_nectar_secretion_01(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                """
                Nectar secretion from the gynoecium (via septal nectaries).
                Floral nectaries present.
                """,
                append_nectary=True,
            ),
            [
                NectarSecretion(structures=["gynoecium"], start=0, end=35),
                FloralNectary(present="1", start=60, end=84),
                FloralNectaryOnAndroecium(present="0"),
                FloralNectaryOnGynoecium(present="1"),
                FloralNectaryOnPerianth(present="0"),
            ],
        )

    def test_nectar_secretion_02(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                """
                Nectar secretion from the perianth, or from the androecium.
                Floral nectaries present.
                """,
                append_nectary=True,
            ),
            [
                NectarSecretion(structures=["androecium", "perianth"], start=0, end=58),
                FloralNectary(present="1", start=60, end=84),
                FloralNectaryOnAndroecium(present="1"),
                FloralNectaryOnGynoecium(present="0"),
                FloralNectaryOnPerianth(present="1"),
            ],
        )

    def test_nectar_secretion_03(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                """
                Nectar secretion from the perianth, or from the androecium.
                Floral nectaries absent.
                """,
                append_nectary=True,
            ),
            [
                NectarSecretion(structures=["androecium", "perianth"], start=0, end=58),
                FloralNectary(present="0", start=60, end=83),
                FloralNectaryOnAndroecium(present="0"),
                FloralNectaryOnGynoecium(present="0"),
                FloralNectaryOnPerianth(present="0"),
            ],
        )

    def test_nectar_secretion_04(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                """
                Nectar secretion from the perianth, or from the androecium.
                """,
                append_nectary=True,
            ),
            [
                NectarSecretion(structures=["androecium", "perianth"], start=0, end=58),
                FloralNectaryOnAndroecium(present="-"),
                FloralNectaryOnGynoecium(present="0"),
                FloralNectaryOnPerianth(present="-"),
            ],
        )

    def test_nectar_secretion_05(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                """
                Floral nectaries present.
                """,
                append_nectary=True,
            ),
            [
                FloralNectary(present="1", start=0, end=24),
                FloralNectaryOnAndroecium(present="?"),
                FloralNectaryOnGynoecium(present="?"),
                FloralNectaryOnPerianth(present="?"),
            ],
        )

    def test_nectar_secretion_06(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                """
                Floral nectaries absent.
                """,
                append_nectary=True,
            ),
            [
                FloralNectary(present="0", start=0, end=23),
                FloralNectaryOnAndroecium(present="-"),
                FloralNectaryOnGynoecium(present="-"),
                FloralNectaryOnPerianth(present="-"),
            ],
        )

    def test_nectar_secretion_07(self):
        self.assertEqual(
            parse(
                "reproductive_type",
                """
                Yada yada yada.
                """,
                append_nectary=True,
            ),
            [
                FloralNectaryOnAndroecium(present="-"),
                FloralNectaryOnGynoecium(present="-"),
                FloralNectaryOnPerianth(present="-"),
            ],
        )
