from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.perianth.fusion_of_perianth import FusionOfPerianth
from angiosperm.pylib.rules.perianth.number_of_petals_fused import NumberOfPetalsFused
from angiosperm.pylib.rules.perianth.symmetry_of_perianth import SymmetryOfPerianth
from angiosperm.pylib.rules.range import Range


def build():
    nlp = base.setup()

    FusionOfPerianth.pipe(nlp)
    SymmetryOfPerianth.pipe(nlp)

    Range.pipe(nlp)
    NumberOfPetalsFused.pipe(nlp)

    return base.teardown(nlp)
