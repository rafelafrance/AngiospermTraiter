from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add


def pipe(nlp: Language):
    add.custom_pipe(nlp, "cleanup", config={"delete": """ range """.split()})


@Language.factory("cleanup")
class Cleanup:
    def __init__(self, nlp: Language, name: str, delete: list[str]):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.delete = delete

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent._.delete or ent.label_ in self.delete:
                continue

            entities.append(ent)

        doc.ents = entities
        return doc


def clear_tokens(ent):
    """Clear tokens in an entity."""
    for token in ent:
        token._.trait = None
        token._.flag = ""
        token._.term = ""
