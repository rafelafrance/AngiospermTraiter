from traiter.pylib.util import compress

from angiosperm.pylib.pipelines import util
from angiosperm.pylib.rules.missing import get_missing_traits
from angiosperm.pylib.rules.nectaries_secretion import get_nectaries_secretion
from angiosperm.pylib.rules.phyllotaxy import get_missing_phyllotaxy


def parse(
    pipeline: str,
    text: str,
    *,
    append_missing=False,
    append_nectary=False,
    append_phyllotaxy=False,
) -> list:
    text = compress(text)
    traits = util.get_traits(pipeline, text)

    if append_missing:
        get_missing_traits(traits)

    if append_nectary:
        get_nectaries_secretion(traits)

    if append_phyllotaxy:
        get_missing_phyllotaxy(traits)

    # from pprint import pp
    # pp(traits)

    return traits
