from traiter.pylib.util import compress

from angiosperm.pylib.pipelines import (
    androecium,
    general_floral,
    perianth,
    reproductive_type,
)

PIPELINES = {
    "androecium": androecium.build(),
    "general_floral": general_floral.build(),
    "perianth": perianth.build(),
    "reproductive_type": reproductive_type.build(),
}


def parse(pipeline: str, text: str) -> list:
    text = compress(text)
    doc = PIPELINES[pipeline](text)
    traits = [e._.trait for e in doc.ents]

    # from pprint import pp
    # pp(traits)

    return traits
