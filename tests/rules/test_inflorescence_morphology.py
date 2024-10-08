import unittest

from angiosperm.pylib.rules.general_floral.inflorescence_morphology import (
    InflorescenceMorphology,
)
from angiosperm.pylib.rules.general_floral.inflorescence_position import (
    InflorescencePosition,
)
from angiosperm.pylib.rules.general_floral.pedicel import Pedicel
from tests.setup import parse


class TestInflorescence(unittest.TestCase):
    def test_inflorescence_01(self):
        self.assertEqual(
            parse(
                "general_floral",
                """Inflorescences terminal, or axillary; usually in cymes, cymose
                corymbs, panicles or umbels, in racemes of panicles,
                or even in heads;""",
            ),
            [
                InflorescencePosition(position="terminal", start=15, end=23),
                InflorescencePosition(position="axillary", start=28, end=36),
                InflorescenceMorphology(
                    morphology="cyme", growth_pattern="determinate", start=49, end=54
                ),
                InflorescenceMorphology(
                    morphology="cyme", growth_pattern="determinate", start=56, end=62
                ),
                InflorescenceMorphology(
                    morphology="raceme-like",
                    growth_pattern="indeterminate",
                    start=63,
                    end=70,
                ),
                InflorescenceMorphology(
                    morphology="panicle",
                    growth_pattern="indeterminate",
                    start=72,
                    end=80,
                ),
                InflorescenceMorphology(
                    morphology="umbel", growth_pattern="indeterminate", start=84, end=90
                ),
                InflorescenceMorphology(
                    morphology="raceme-like",
                    growth_pattern="indeterminate",
                    start=95,
                    end=102,
                ),
                InflorescenceMorphology(
                    morphology="panicle",
                    growth_pattern="indeterminate",
                    start=106,
                    end=114,
                ),
                InflorescenceMorphology(
                    morphology="globose capitula",
                    start=127,
                    end=132,
                ),
            ],
        )

    def test_inflorescence_02(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                "general_floral",
                """The ultimate inflorescence units racemose.
                Inflorescences pedunculate heads, short racemes or compact umbels,
                or sometimes reduced to a single flower.""",
            ),
            [
                InflorescenceMorphology(
                    morphology="raceme-like",
                    growth_pattern="indeterminate",
                    start=33,
                    end=41,
                ),
                Pedicel(start=58, end=69, present=True),
                InflorescenceMorphology(
                    morphology="globose capitula",
                    start=70,
                    end=75,
                ),
                InflorescenceMorphology(
                    morphology="raceme-like",
                    growth_pattern="indeterminate",
                    start=83,
                    end=90,
                ),
                InflorescenceMorphology(
                    morphology="umbel",
                    growth_pattern="indeterminate",
                    start=102,
                    end=108,
                ),
            ],
        )
