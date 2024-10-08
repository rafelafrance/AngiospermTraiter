import unittest

from angiosperm.pylib.rules.number_of_fertile_stamens import (
    NumberOfFertileStamens,
)
from tests.setup import parse


class TestFlowerCount(unittest.TestCase):
    def test_number_of_fertile_stamens_01(self):
        self.assertEqual(
            parse("androecium", "fertile stamens (8–)10(–16)."),
            [NumberOfFertileStamens(min=8, low=10, max=16, start=0, end=27)],
        )

    def test_number_of_fertile_stamens_02(self):
        self.assertEqual(
            parse("androecium", "8–10–fertile stamens"),
            [NumberOfFertileStamens(low=8, high=10, start=0, end=20)],
        )
