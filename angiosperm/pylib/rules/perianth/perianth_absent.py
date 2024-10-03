from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.perianth.perianth_presence import PerianthPresence


def pipe(nlp: Language):
    add.custom_pipe(nlp, "perianth_present")


@Language.factory("perianth_present")
class PerianthPresent:
    def __init__(self, nlp: Language, name: str):
        super().__init__()
        self.nlp = nlp
        self.name = name

    def __call__(self, doc: Doc) -> Doc:
        entities = list(doc.ents)
        entities.append(PerianthPresence.perianth_presence(present=False))
        doc.ents = entities
        return doc
