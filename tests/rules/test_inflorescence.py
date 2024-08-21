import unittest

from angiosperm.pylib.rules.inflorescence import Inflorescence
from angiosperm.pylib.rules.inflorescence_position import InflorescencePosition
from tests.setup import parse


class TestInflorescence(unittest.TestCase):
    def test_inflorescence_01(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                """Inflorescences terminal, or axillary; usually in cymes, cymose
                corymbs, panicles or umbels, in racemes of panicles,
                or even in heads;"""
            ),
            [
                InflorescencePosition(position="terminal", start=15, end=23),
                InflorescencePosition(position="axillary", start=28, end=36),
                Inflorescence(
                    morphology="cyme", growth_pattern="determinate", start=49, end=54
                ),
                Inflorescence(
                    morphology="cymose", growth_pattern="determinate", start=56, end=62
                ),
                Inflorescence(
                    morphology="raceme-like",
                    growth_pattern="indeterminate",
                    start=63,
                    end=70,
                ),
                Inflorescence(
                    morphology="panicle",
                    growth_pattern="indeterminate",
                    start=72,
                    end=80,
                ),
                Inflorescence(morphology="umbel", start=84, end=90),
                Inflorescence(
                    morphology="raceme-like",
                    growth_pattern="indeterminate",
                    start=95,
                    end=102,
                ),
                Inflorescence(
                    morphology="panicle",
                    growth_pattern="indeterminate",
                    start=106,
                    end=114,
                ),
            ],
        )

    def test_inflorescence_02(self):
        self.assertEqual(
            parse(
                """The ultimate inflorescence units racemose.
                Inflorescences pedunculate heads, short racemes or compact umbels,
                or sometimes reduced to a single flower."""
            ),
            [
                Inflorescence(
                    morphology="raceme-like",
                    growth_pattern="indeterminate",
                    start=33,
                    end=41,
                ),
                Inflorescence(
                    morphology="raceme-like",
                    growth_pattern="indeterminate",
                    start=83,
                    end=90,
                ),
                Inflorescence(morphology="umbel", start=102, end=108),
            ],
        )
