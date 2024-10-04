from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.perianth.clawed_petal import ClawedPetal
from angiosperm.pylib.rules.perianth.fusion_of_perianth import FusionOfPerianth
from angiosperm.pylib.rules.perianth.number_of_perianth_whorls import (
    NumberOfPerianthWhorls,
)
from angiosperm.pylib.rules.perianth.number_of_petals_fused import NumberOfPetalsFused
from angiosperm.pylib.rules.perianth.perianth_differentiation import (
    PerianthDifferentiation,
)
from angiosperm.pylib.rules.perianth.perianth_margin import PerianthMargin
from angiosperm.pylib.rules.perianth.perianth_merism import PerianthMerism
from angiosperm.pylib.rules.perianth.perianth_shape import PerianthShape
from angiosperm.pylib.rules.perianth.saccate_perianth import SaccatePerianth
from angiosperm.pylib.rules.perianth.symmetry_of_perianth import SymmetryOfPerianth
from angiosperm.pylib.rules.range import Range


def build():
    nlp = base.setup()

    FusionOfPerianth.pipe(nlp)
    SymmetryOfPerianth.pipe(nlp)
    PerianthMerism.pipe(nlp)
    PerianthDifferentiation.pipe(nlp)
    SaccatePerianth.pipe(nlp)
    PerianthMargin.pipe(nlp)
    ClawedPetal.pipe(nlp)
    PerianthShape.pipe(nlp)

    Range.pipe(nlp)
    NumberOfPetalsFused.pipe(nlp)
    NumberOfPerianthWhorls.pipe(nlp)

    return base.teardown(nlp)
