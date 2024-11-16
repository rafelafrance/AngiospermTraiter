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


@dataclass
class Pipeline:
    pattern: str
    pipeline: Any


PIPELINES = {
    "androecium": Pipeline("androecium", androecium.build()),
    "general_floral": Pipeline("inflorescence", general_floral.build()),
    "gynoecium": Pipeline("gynoecium", gynoecium.build()),
    "leaf_anatomy": Pipeline("leaf anatomy", leaf.build()),
    "perianth": Pipeline("perianth", perianth.build()),
    "reproductive_type": Pipeline("reproductive type", reproductive_type.build()),
}


def get_traits(key: str, text: str):
    doc = PIPELINES[key].pipeline(text)
    traits = [e._.trait for e in doc.ents]
    return traits
