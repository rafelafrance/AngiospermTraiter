import unittest

from angiosperm.pylib.rules.androecium.staminodes import Staminodes
from tests.setup import parse


class TestExtrafloralNectary(unittest.TestCase):
    def test_extrafloral_nectary_01(self):
        self.assertEqual(
            parse("androecium", "or including staminodes"),
            [
                Staminodes(present=True, start=13, end=23),
            ],
        )
