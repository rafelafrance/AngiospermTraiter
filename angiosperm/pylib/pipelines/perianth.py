from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.clawed_petal import ClawedPetal
from angiosperm.pylib.rules.fusion_of_perianth import FusionOfPerianth
from angiosperm.pylib.rules.number_of_perianth_whorls import NumberOfPerianthWhorls
from angiosperm.pylib.rules.number_of_petals_fused import NumberOfPetalsFused
from angiosperm.pylib.rules.perianth_differentiation import PerianthDifferentiation
from angiosperm.pylib.rules.perianth_margin import PerianthMargin
from angiosperm.pylib.rules.perianth_merism import PerianthMerism
from angiosperm.pylib.rules.perianth_presence import PerianthPresence
from angiosperm.pylib.rules.phyllotaxy import Phyllotaxy

# from angiosperm.pylib.rules.perianth_shape import PerianthShape
from angiosperm.pylib.rules.range import Range
from angiosperm.pylib.rules.saccate_perianth import SaccatePerianth
from angiosperm.pylib.rules.symmetry_of_perianth import SymmetryOfPerianth


def build():
    nlp = base.setup()

    Range.pipe(nlp)
    NumberOfPetalsFused.pipe(nlp)
    NumberOfPerianthWhorls.pipe(nlp)

    FusionOfPerianth.pipe(nlp)
    SymmetryOfPerianth.pipe(nlp)
    PerianthMerism.pipe(nlp)
    PerianthDifferentiation.pipe(nlp)
    SaccatePerianth.pipe(nlp)
    PerianthMargin.pipe(nlp)
    ClawedPetal.pipe(nlp)
    # PerianthShape.pipe(nlp)

    # Need to be last because they overlap with other traits
    PerianthPresence.pipe(nlp)

    Phyllotaxy.pipe(nlp)
    Phyllotaxy.structure = "perianth"

    return base.teardown(nlp)
