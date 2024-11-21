import unittest

from angiosperm.pylib.rules.number_of_perianth_whorls import NumberOfPerianthWhorls
from angiosperm.pylib.rules.phyllotaxy import Phyllotaxy
from tests.setup import parse


class TestPhyllotaxy(unittest.TestCase):
    def test_phyllotaxy_01(self):
        self.assertEqual(
            parse(
                "perianth",
                "the whorls sometimes rather different",
                append_phyllotaxy=True,
            ),
            [
                Phyllotaxy(phyllotaxy=["0"], start=4, end=10),
            ],
        )

    def test_phyllotaxy_02(self):
        self.assertEqual(
            parse("perianth", "1 whorled", append_phyllotaxy=True),
            [
                NumberOfPerianthWhorls(low=1, start=0, end=9),
                Phyllotaxy(_trait="perianth_phyllotaxy", phyllotaxy=["0"]),
            ],
        )
