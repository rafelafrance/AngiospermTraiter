import unittest

from angiosperm.pylib.rules.symmetry_of_perianth import SymmetryOfPerianth
from tests.setup import parse


class TestSymmetryOfPerianth(unittest.TestCase):
    def test_symmetry_of_perianth_01(self):
        self.assertEqual(
            parse("perianth", "or joined (symmetric or asymmetric,"),
            [
                SymmetryOfPerianth(symmetry="symmetric", start=11, end=20),
                SymmetryOfPerianth(symmetry="asymmetric", start=24, end=34),
            ],
        )
