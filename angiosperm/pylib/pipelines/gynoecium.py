from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.number_of_carpels import NumberOfCarpels
from angiosperm.pylib.rules.range import Range


def build():
    nlp = base.setup()

    Range.pipe(nlp)
    NumberOfCarpels.pipe(nlp)

    return base.teardown(nlp)
