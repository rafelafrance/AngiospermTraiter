from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.bract import Bract
from angiosperm.pylib.rules.flower_count import FlowerCount
from angiosperm.pylib.rules.flower_grouping import FlowerGrouping
from angiosperm.pylib.rules.inflorescence import Inflorescence
from angiosperm.pylib.rules.inflorescence_position import InflorescencePosition
from angiosperm.pylib.rules.ovary_position import OvaryPosition
from angiosperm.pylib.rules.range import Range
from angiosperm.pylib.rules.sexual_system import SexualSystem
from angiosperm.pylib.rules.structural_sex import StructuralSex


def build():
    nlp = base.setup()

    SexualSystem.pipe(nlp)
    StructuralSex.pipe(nlp)
    OvaryPosition.pipe(nlp)
    FlowerGrouping.pipe(nlp)
    Inflorescence.pipe(nlp)
    InflorescencePosition.pipe(nlp)
    Bract.pipe(nlp)

    Range.pipe(nlp)
    FlowerCount.pipe(nlp)

    return base.teardown(nlp)
