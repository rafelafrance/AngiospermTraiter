from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.number_of_carpels import NumberOfCarpels
from angiosperm.pylib.rules.number_of_whorls import NumberOfWhorls
from angiosperm.pylib.rules.phyllotaxy import Phyllotaxy
from angiosperm.pylib.rules.range import Range


def build():
    structure = "gynoecium"

    nlp = base.setup()

    Range.pipe(nlp)
    NumberOfCarpels.pipe(nlp)

    NumberOfWhorls.structure = structure
    NumberOfWhorls.pipe(nlp)

    Phyllotaxy.structure = structure
    Phyllotaxy.pipe(nlp)

    return base.teardown(nlp)
