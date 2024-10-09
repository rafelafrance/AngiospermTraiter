import unittest

from angiosperm.pylib.rules.number_of_fertile_stamens import (
    NumberOfFertileStamens,
)
from tests.setup import parse


class TestFlowerCount(unittest.TestCase):
    def test_number_of_fertile_stamens_01(self):
        self.assertEqual(
            parse("androecium", "Androecium 5."),
            [NumberOfFertileStamens(low=5, start=0, end=12)],
        )

    def test_number_of_fertile_stamens_02(self):
        self.assertEqual(
            parse("androecium", "Androecium (1–)10–100 (usually many)."),
            [NumberOfFertileStamens(min=1, low=10, high=100, start=0, end=21)],
        )

    def test_number_of_fertile_stamens_03(self):
        self.assertEqual(
            parse("androecium", "Androecium 4, or 5–8."),
            [
                NumberOfFertileStamens(low=4, start=0, end=12),
                NumberOfFertileStamens(low=5, high=8, start=17, end=20),
            ],
        )
