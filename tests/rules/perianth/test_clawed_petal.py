import unittest

from angiosperm.pylib.rules.perianth.clawed_petal import ClawedPetal
from tests.setup import parse


class TestFloralNectaryOnAndroecium(unittest.TestCase):
    def test_clawed_petal_01(self):
        self.assertEqual(
            parse("perianth", "Petals slightly clawed"),
            [
                ClawedPetal(present=True, start=16, end=22),
            ],
        )
