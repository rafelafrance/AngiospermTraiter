from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.androecium.number_of_fertile_stamens import (
    NumberOfFertileStamens,
)
from angiosperm.pylib.rules.range import Range


def build():
    nlp = base.setup()

    Range.pipe(nlp)
    NumberOfFertileStamens.pipe(nlp)

    return base.teardown(nlp)
