import unittest

from angiosperm.pylib.rules.inflorescence_morphology import (
    InflorescenceMorphology,
)
from angiosperm.pylib.rules.inflorescence_position import (
    InflorescencePosition,
)
from angiosperm.pylib.rules.pedicel import Pedicel
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
                InflorescencePosition(position="0", start=15, end=23),
                InflorescencePosition(position="1", start=28, end=36),
                InflorescenceMorphology(
                    morphology="1", growth_pattern="1", start=49, end=54
                ),
                InflorescenceMorphology(
                    morphology="1", growth_pattern="1", start=56, end=62
                ),
                InflorescenceMorphology(
                    morphology="2",
                    growth_pattern="0",
                    start=63,
                    end=70,
                ),
                InflorescenceMorphology(
                    morphology="0",
                    growth_pattern="0",
                    start=72,
                    end=80,
                ),
                InflorescenceMorphology(
                    morphology="1", growth_pattern="0", start=84, end=90
                ),
                InflorescenceMorphology(
                    morphology="2",
                    growth_pattern="0",
                    start=95,
                    end=102,
                ),
                InflorescenceMorphology(
                    morphology="0",
                    growth_pattern="0",
                    start=106,
                    end=114,
                ),
                InflorescenceMorphology(morphology="0", start=127, end=132),
            ],
        )

    def test_inflorescence_02(self):
        self.assertEqual(
            parse(
                "general_floral",
                """The ultimate inflorescence units racemose.
                Inflorescences pedunculate heads, short racemes or compact umbels,
                or sometimes reduced to a single flower.""",
            ),
            [
                InflorescenceMorphology(
                    morphology="2",
                    growth_pattern="0",
                    start=33,
                    end=41,
                ),
                Pedicel(start=58, end=69, present="1"),
                InflorescenceMorphology(morphology="0", start=70, end=75),
                InflorescenceMorphology(
                    morphology="2",
                    growth_pattern="0",
                    start=83,
                    end=90,
                ),
                InflorescenceMorphology(
                    morphology="1",
                    growth_pattern="0",
                    start=102,
                    end=108,
                ),
            ],
        )
