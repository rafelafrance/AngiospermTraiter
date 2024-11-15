import unittest

from angiosperm.pylib.rules.bracts import Bracts
from angiosperm.pylib.rules.petaloid_bracts import PetaloidBracts
from tests.setup import parse


class TestBracts(unittest.TestCase):
    def test_bracts_01(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                "general_floral",
                "with involucral bracts, or without involucral bracts;",
                append_missing=True,
            ),
            [
                Bracts(present="1", start=5, end=15),
                Bracts(present="0", start=27, end=45),
                PetaloidBracts(present="?"),
            ],
        )

    def test_bracts_02(self):
        self.assertEqual(
            parse("general_floral", "Nothing about this trait", append_missing=True),
            [
                Bracts(present="?"),
                PetaloidBracts(present="?"),
            ],
        )
