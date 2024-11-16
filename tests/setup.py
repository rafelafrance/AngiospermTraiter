from traiter.pylib.util import compress

from angiosperm.pylib.pipelines import util
from angiosperm.pylib.rules.missing import get_missing
from angiosperm.pylib.rules.nectaries_secretion import get_nectaries_secretion


def parse(
    pipeline: str, text: str, *, append_missing=False, append_nectary=False
) -> list:
    text = compress(text)
    traits = util.get_traits(pipeline, text)

    if append_missing:
        get_missing(traits)

    if append_nectary:
        get_nectaries_secretion(traits)

    # from pprint import pp
    # pp(traits)

    return traits
