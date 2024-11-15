import unittest

from angiosperm.pylib.rules.inflorescence_position import InflorescencePosition
from tests.setup import parse


class TestInflorescencePosition(unittest.TestCase):
    def test_inflorescence_position_01(self):
        self.assertEqual(
            parse("general_floral", """terminal, or axillary;"""),
            [
                InflorescencePosition(position="terminal", start=0, end=8),
                InflorescencePosition(position="axillary", start=13, end=21),
            ],
        )
