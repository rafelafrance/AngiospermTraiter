import spacy
from traiter.pylib.pipes import extensions, tokenizer

from angiosperm.pylib.rules import cleanup


def setup():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)
    return nlp


def teardown(nlp):
    cleanup.pipe(nlp)
    return nlp
