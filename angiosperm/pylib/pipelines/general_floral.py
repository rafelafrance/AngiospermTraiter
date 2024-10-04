from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.general_floral.bracts import Bracts
from angiosperm.pylib.rules.general_floral.extrafloral_nectary import ExtrafloralNectary
from angiosperm.pylib.rules.general_floral.floral_nectary_on_androecium import (
    FloralNectaryOnAndroecium,
)
from angiosperm.pylib.rules.general_floral.floral_nectary_on_gynoecium import (
    FloralNectaryOnGynoecium,
)
from angiosperm.pylib.rules.general_floral.floral_nectary_on_perianth import (
    FloralNectaryOnPerianth,
)
from angiosperm.pylib.rules.general_floral.flower_grouping import FlowerGrouping
from angiosperm.pylib.rules.general_floral.flowers_in_an_inflorescence import (
    FlowersInAnInflorescence,
)
from angiosperm.pylib.rules.general_floral.inflorescence_morphology import (
    InflorescenceMorphology,
)
from angiosperm.pylib.rules.general_floral.inflorescence_position import (
    InflorescencePosition,
)
from angiosperm.pylib.rules.general_floral.ovary_position import OvaryPosition
from angiosperm.pylib.rules.general_floral.pedicel import Pedicel
from angiosperm.pylib.rules.general_floral.petaloid_bracts import PetaloidBracts
from angiosperm.pylib.rules.range import Range


def build():
    nlp = base.setup()

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
    ExtrafloralNectary.pipe(nlp)

    Range.pipe(nlp)
    FlowersInAnInflorescence.pipe(nlp)

    return base.teardown(nlp)
