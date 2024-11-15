import unittest

from angiosperm.pylib.rules.staminodes import Staminodes
from tests.setup import parse


class TestStaminodes(unittest.TestCase):
    def test_staminodes_01(self):
        self.assertEqual(
            parse("androecium", "or including staminodes"),
            [
                Staminodes(present="1", start=13, end=23),
            ],
        )
