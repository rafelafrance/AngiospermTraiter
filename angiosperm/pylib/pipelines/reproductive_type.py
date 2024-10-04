from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.reproductive_type.plant_sexual_system import (
    PlantSexualSystem,
)
from angiosperm.pylib.rules.reproductive_type.structural_sex_of_flowers import (
    StructuralSexOfFlowers,
)


def build():
    nlp = base.setup()

    PlantSexualSystem.pipe(nlp)
    StructuralSexOfFlowers.pipe(nlp)

    return base.teardown(nlp)
