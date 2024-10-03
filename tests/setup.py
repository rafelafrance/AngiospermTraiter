from traiter.pylib.util import compress

from angiosperm.pylib.pipelines import androecium, general_floral, perianth

ANDROECIUM = androecium.build()
GENERAL_FLORAL = general_floral.build()
PERIANTH = perianth.build()


def androecium_parse(text: str) -> list:
    text = compress(text)
    doc = ANDROECIUM(text)
    traits = [e._.trait for e in doc.ents]

    # from pprint import pp
    # pp(traits)

    return traits


def general_floral_parse(text: str) -> list:
    text = compress(text)
    doc = GENERAL_FLORAL(text)
    traits = [e._.trait for e in doc.ents]

    # from pprint import pp
    # pp(traits)

    return traits


def perianth_parse(text: str) -> list:
    text = compress(text)
    doc = PERIANTH(text)
    traits = [e._.trait for e in doc.ents]

    # from pprint import pp
    # pp(traits)

    return traits
