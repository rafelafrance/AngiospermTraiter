from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.extrafloral_nectary import ExtrafloralNectary
from angiosperm.pylib.rules.floral_nectary_on_androecium import (
    FloralNectaryOnAndroecium,
)
from angiosperm.pylib.rules.floral_nectary_on_gynoecium import FloralNectaryOnGynoecium
from angiosperm.pylib.rules.floral_nectary_on_perianth import FloralNectaryOnPerianth
from angiosperm.pylib.rules.plant_sexual_system import PlantSexualSystem
from angiosperm.pylib.rules.structural_sex_of_flowers import StructuralSexOfFlowers


def build():
    nlp = base.setup()

    PlantSexualSystem.pipe(nlp)
    StructuralSexOfFlowers.pipe(nlp)

    FloralNectaryOnAndroecium.pipe(nlp)
    FloralNectaryOnGynoecium.pipe(nlp)
    FloralNectaryOnPerianth.pipe(nlp)
    ExtrafloralNectary.pipe(nlp)

    return base.teardown(nlp)
