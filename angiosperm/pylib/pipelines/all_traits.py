from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.plant_sexual_system import PlantSexualSystem
from angiosperm.pylib.rules.structural_sex_of_flowers import StructuralSexOfFlowers


def build():
    nlp = base.setup()

    PlantSexualSystem.pipe(nlp)
    StructuralSexOfFlowers.pipe(nlp)
    # OvaryPosition.pipe(nlp)
    # FlowerGrouping.pipe(nlp)
    # InflorescencePosition.pipe(nlp)
    # Bract.pipe(nlp)
    #
    # Range.pipe(nlp)
    # FlowerCount.pipe(nlp)

    return base.teardown(nlp)
