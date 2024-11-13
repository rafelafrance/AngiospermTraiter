from angiosperm.pylib.pipelines import (
    androecium,
    general_floral,
    gynoecium,
    leaf,
    perianth,
    reproductive_type,
)
from angiosperm.pylib.rules.bracts import Bracts

PIPELINES = {
    "androecium": androecium.build(),
    "general_floral": general_floral.build(),
    "gynoecium": gynoecium.build(),
    "leaf": leaf.build(),
    "perianth": perianth.build(),
    "reproductive_type": reproductive_type.build(),
}

MISSING = {
    "bracts": Bracts,
}


def get_traits(pipeline: str, text: str, *, append_missing=True):
    doc = PIPELINES[pipeline](text)
    traits = [e._.trait for e in doc.ents]
    if append_missing:
        get_missing(traits)
    return traits


def get_missing(traits):
    found = {t._trait for t in traits}
    for trait_name, cls in MISSING.items():
        if trait_name not in found:
            trait = cls(_trait=trait_name, present="?")
            traits.append(trait)
