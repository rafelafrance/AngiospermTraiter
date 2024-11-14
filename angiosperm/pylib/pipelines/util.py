from angiosperm.pylib.pipelines import (
    androecium,
    general_floral,
    gynoecium,
    leaf,
    perianth,
    reproductive_type,
)
from angiosperm.pylib.rules.missing import get_missing
from angiosperm.pylib.rules.nectaries_secretion import get_nectaries_secretion

PIPELINES = {
    "androecium": androecium.build(),
    "general_floral": general_floral.build(),
    "gynoecium": gynoecium.build(),
    "leaf": leaf.build(),
    "perianth": perianth.build(),
    "reproductive_type": reproductive_type.build(),
}


def get_traits(pipeline: str, text: str, *, append_missing=True, append_nectary=True):
    doc = PIPELINES[pipeline](text)
    traits = [e._.trait for e in doc.ents]

    if append_missing:
        get_missing(traits)

    if append_nectary:
        get_nectaries_secretion(traits)

    return traits
