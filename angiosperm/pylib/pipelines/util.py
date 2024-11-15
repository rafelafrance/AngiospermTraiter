from dataclasses import dataclass
from typing import Any

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


@dataclass
class Pipeline:
    pattern: str
    pipeline: Any


PIPELINES = {
    "androecium": Pipeline("androecium", androecium.build()),
    "general_floral": Pipeline("floral", general_floral.build()),
    "gynoecium": Pipeline("gynoecium", gynoecium.build()),
    "leaf_anatomy": Pipeline("leaf anatomy", leaf.build()),
    "perianth": Pipeline("perianth", perianth.build()),
    "reproductive_type": Pipeline("reproductive type", reproductive_type.build()),
}


def get_traits(pipeline: str, text: str, *, append_missing=True, append_nectary=True):
    doc = PIPELINES[pipeline].pipeline(text)
    traits = [e._.trait for e in doc.ents]

    if append_missing:
        get_missing(traits)

    if append_nectary:
        get_nectaries_secretion(traits)

    return traits
