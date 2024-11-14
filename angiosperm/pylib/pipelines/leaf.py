from angiosperm.pylib.pipelines import base


def build():
    nlp = base.setup()

    return base.teardown(nlp)
