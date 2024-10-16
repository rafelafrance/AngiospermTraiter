from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.bracts import Bracts
from angiosperm.pylib.rules.flower_grouping import FlowerGrouping
from angiosperm.pylib.rules.inflorescence_morphology import InflorescenceMorphology
from angiosperm.pylib.rules.inflorescence_position import InflorescencePosition
from angiosperm.pylib.rules.ovary_position import OvaryPosition
from angiosperm.pylib.rules.pedicel import Pedicel
from angiosperm.pylib.rules.petaloid_bracts import PetaloidBracts


def build():
    nlp = base.setup()

    FlowerGrouping.pipe(nlp)
    InflorescencePosition.pipe(nlp)
    InflorescenceMorphology.pipe(nlp)
    Bracts.pipe(nlp)
    PetaloidBracts.pipe(nlp)
    OvaryPosition.pipe(nlp)
    Pedicel.pipe(nlp)

    return base.teardown(nlp)
