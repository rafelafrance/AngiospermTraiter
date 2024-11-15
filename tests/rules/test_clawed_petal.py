import unittest

from angiosperm.pylib.rules.clawed_petal import ClawedPetal
from tests.setup import parse


class TestClawedPetal(unittest.TestCase):
    def test_clawed_petal_01(self):
        self.assertEqual(
            parse("perianth", "Petals slightly clawed"),
            [
                ClawedPetal(present="1", start=16, end=22),
            ],
        )
