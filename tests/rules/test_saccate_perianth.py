import unittest

from angiosperm.pylib.rules.saccate_perianth import SaccatePerianth
from tests.setup import parse


class TestFloralNectaryOnAndroecium(unittest.TestCase):
    def test_saccate_perianth_01(self):
        self.assertEqual(
            parse("perianth", "(or saccate, anteriorly)"),
            [
                SaccatePerianth(present="1", start=4, end=11),
            ],
        )
