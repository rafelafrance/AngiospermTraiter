from angiosperm.pylib.pipelines import base
from angiosperm.pylib.rules.extrafloral_nectary import ExtrafloralNectary


def build():
    nlp = base.setup()

    ExtrafloralNectary.pipe(nlp)

    return base.teardown(nlp)
