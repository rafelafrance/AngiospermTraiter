from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.floral_nectary import FloralNectary
from angiosperm.pylib.rules.nectar_secretion import NectarSecretion
from angiosperm.pylib.rules.plant_sexual_system import PlantSexualSystem
from angiosperm.pylib.rules.structural_sex_of_flowers import StructuralSexOfFlowers


def build():
    nlp = base.setup()

    PlantSexualSystem.pipe(nlp)
    StructuralSexOfFlowers.pipe(nlp)

    FloralNectary.pipe(nlp)
    NectarSecretion.pipe(nlp)

    return base.teardown(nlp)
