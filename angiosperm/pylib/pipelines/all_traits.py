from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.bracts import Bracts
from angiosperm.pylib.rules.floral_nectary_on_androecium import (
    FloralNectaryOnAndroecium,
)
from angiosperm.pylib.rules.floral_nectary_on_gynoecium import FloralNectaryOnGynoecium
from angiosperm.pylib.rules.floral_nectary_on_perianth import FloralNectaryOnPerianth
from angiosperm.pylib.rules.flower_grouping import FlowerGrouping
from angiosperm.pylib.rules.inflorescence_morphology import InflorescenceMorphology
from angiosperm.pylib.rules.inflorescence_position import InflorescencePosition
from angiosperm.pylib.rules.number_of_flowers_in_an_inflorescence import (
    NumberOfFlowersInAnInflorescence,
)
from angiosperm.pylib.rules.ovary_position import OvaryPosition
from angiosperm.pylib.rules.pedicel import Pedicel
from angiosperm.pylib.rules.petaloid_bracts import PetaloidBracts
from angiosperm.pylib.rules.plant_sexual_system import PlantSexualSystem
from angiosperm.pylib.rules.range import Range
from angiosperm.pylib.rules.structural_sex_of_flowers import StructuralSexOfFlowers


def build():
    nlp = base.setup()

    PlantSexualSystem.pipe(nlp)
    StructuralSexOfFlowers.pipe(nlp)
    FlowerGrouping.pipe(nlp)
    InflorescencePosition.pipe(nlp)
    InflorescenceMorphology.pipe(nlp)
    Bracts.pipe(nlp)
    PetaloidBracts.pipe(nlp)
    OvaryPosition.pipe(nlp)
    Pedicel.pipe(nlp)
    FloralNectaryOnGynoecium.pipe(nlp)
    FloralNectaryOnAndroecium.pipe(nlp)
    FloralNectaryOnPerianth.pipe(nlp)

    Range.pipe(nlp)
    NumberOfFlowersInAnInflorescence.pipe(nlp)

    return base.teardown(nlp)
