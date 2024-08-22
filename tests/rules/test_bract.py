import unittest

from angiosperm.pylib.rules.bract import Bract
from tests.setup import parse


class TestBract(unittest.TestCase):
    def test_bract_01(self):
        self.assertEqual(
            parse("with involucral bracts, or without involucral bracts;"),
            [
                Bract(present=True, start=5, end=22),
                Bract(present=False, start=27, end=52),
            ],
        )
