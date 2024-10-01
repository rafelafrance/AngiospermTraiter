import unittest

from angiosperm.pylib.rules.bracts import Bracts
from tests.setup import parse


class TestBract(unittest.TestCase):
    def test_bract_01(self):
        self.assertEqual(
            parse("with involucral bracts, or without involucral bracts;"),
            [
                Bracts(present=True, start=5, end=15),
                Bracts(present=False, start=27, end=45),
            ],
        )
