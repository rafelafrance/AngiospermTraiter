import unittest

from angiosperm.pylib.rules.floral_nectary_on_androecium import (
    FloralNectaryOnAndroecium,
)
from tests.setup import parse


class TestFloralNectaryOnAndroecium(unittest.TestCase):
    def test_floral_nectary_on_androecium_01(self):
        self.assertEqual(
            parse("floral nectaries on androecium"),
            [
                FloralNectaryOnAndroecium(present=True, start=0, end=30),
            ],
        )
