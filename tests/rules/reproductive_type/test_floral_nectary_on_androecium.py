import unittest

from angiosperm.pylib.rules.reproductive_type.floral_nectary_on_androecium import (
    FloralNectaryOnAndroecium,
)
from tests.setup import parse


class TestFloralNectaryOnAndroecium(unittest.TestCase):
    def test_floral_nectary_on_androecium_01(self):
        self.assertEqual(
            parse("reproductive_type", "Nectar secretion from the androecium"),
            [
                FloralNectaryOnAndroecium(present=True, start=0, end=36),
            ],
        )
