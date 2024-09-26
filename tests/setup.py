from traiter.pylib.util import compress

from angiosperm.pylib.pipelines import all_traits

PIPELINE = all_traits.build()


def parse(text: str) -> list:
    text = compress(text)
    doc = PIPELINE(text)
    traits = [e._.trait for e in doc.ents]

    # from pprint import pp
    # pp(traits)

    return traits
