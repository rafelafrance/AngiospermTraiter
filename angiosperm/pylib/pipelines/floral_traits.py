from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.bracts import Bract
from angiosperm.pylib.rules.flower_grouping import FlowerGrouping
from angiosperm.pylib.rules.inflorescence_position import InflorescencePosition
from angiosperm.pylib.rules.number_of_flowers_in_an_inflorescence import FlowerCount
from angiosperm.pylib.rules.ovary_position import OvaryPosition
from angiosperm.pylib.rules.plant_sexual_system import PlantSexualSystem
from angiosperm.pylib.rules.range import Range
from angiosperm.pylib.rules.structural_sex_of_flowers import StructuralSexOfFlowers
from junk.inflorescence import Inflorescence

# from traiter.pylib.pipes import debug


def build():
    nlp = base.setup()

    PlantSexualSystem.pipe(nlp)
    StructuralSexOfFlowers.pipe(nlp)
    OvaryPosition.pipe(nlp)
    FlowerGrouping.pipe(nlp)
    Inflorescence.pipe(nlp)
    InflorescencePosition.pipe(nlp)
    Bract.pipe(nlp)

    Range.pipe(nlp)
    FlowerCount.pipe(nlp)

    return base.teardown(nlp)
