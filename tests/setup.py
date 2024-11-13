from traiter.pylib.util import compress

from angiosperm.pylib.pipelines import util


def parse(pipeline: str, text: str, *, append_missing=False) -> list:
    text = compress(text)
    traits = util.get_traits(pipeline, text, append_missing=append_missing)

    # from pprint import pp
    # pp(traits)

    return traits
