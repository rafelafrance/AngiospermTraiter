import unittest

from angiosperm.pylib.rules.perianth_shape import PerianthShape
from tests.setup import parse


class TestPerianthShape(unittest.TestCase):
    def test_perianth_shape_01(self):
        self.assertEqual(
            parse("perianth", "shortly campanulate;"),
            [
                PerianthShape(shape="bell-shaped", start=8, end=19),
            ],
        )
