import unittest

from angiosperm.pylib.rules.bracts import Bracts
from angiosperm.pylib.rules.extrafloral_nectary import ExtrafloralNectary
from angiosperm.pylib.rules.petaloid_bracts import PetaloidBracts
from tests.setup import parse


class TestExtrafloralNectary(unittest.TestCase):
    def test_extrafloral_nectary_01(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                "leaf_anatomy",
                "often with a pair of glands or extrafloral nectaries",
                append_missing=True,
            ),
            [
                ExtrafloralNectary(present="1", start=31, end=52),
                Bracts(present="?"),
                PetaloidBracts(present="?"),
            ],
        )

    def test_extrafloral_nectary_02(self):
        self.assertEqual(
            parse("leaf_anatomy", "Ssh, don't mention them!", append_missing=True),
            [
                Bracts(present="?"),
                PetaloidBracts(present="?"),
                ExtrafloralNectary(present="0"),
            ],
        )
