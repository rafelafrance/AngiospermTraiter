from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.androecium_structural_whorls import (
    NumberOfAndroeciumWhorls,
)
from angiosperm.pylib.rules.exserted_stamens import ExsertedStamens
from angiosperm.pylib.rules.filament_length import FilamentLength
from angiosperm.pylib.rules.filament_width import FilamentWidth
from angiosperm.pylib.rules.fusion_of_filaments import FusionOfFilaments
from angiosperm.pylib.rules.number_of_fertile_stamens import (
    NumberOfFertileStamens,
)
from angiosperm.pylib.rules.petaloid_staminodes import PetaloidStaminodes
from angiosperm.pylib.rules.range import Range
from angiosperm.pylib.rules.relative_lengths_of_stamens import (
    RelativeLengthsOfStamens,
)
from angiosperm.pylib.rules.stamen_position import StamenPosition
from angiosperm.pylib.rules.staminodes import Staminodes


def build():
    nlp = base.setup()

    Range.pipe(nlp)
    NumberOfFertileStamens.pipe(nlp)
    NumberOfAndroeciumWhorls.pipe(nlp)

    RelativeLengthsOfStamens.pipe(nlp)
    PetaloidStaminodes.pipe(nlp)
    ExsertedStamens.pipe(nlp)
    StamenPosition.pipe(nlp)
    FilamentLength.pipe(nlp)
    FilamentWidth.pipe(nlp)
    FusionOfFilaments.pipe(nlp)

    Staminodes.pipe(nlp)

    return base.teardown(nlp)
