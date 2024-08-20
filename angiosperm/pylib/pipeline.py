import spacy
from traiter.pylib.pipes import extensions, sentence, tokenizer

from angiosperm.pylib.rules.sexual_system import SexualSystem
from angiosperm.pylib.rules.structural_sex import StructuralSex

# from traiter.pylib.pipes import debug


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)

    config = {"base_model": "en_core_web_md"}
    nlp.add_pipe(sentence.SENTENCES, config=config, before="parser")

    SexualSystem.pipe(nlp)
    StructuralSex.pipe(nlp)

    return nlp
