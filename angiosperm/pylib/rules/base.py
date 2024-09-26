from dataclasses import dataclass

from spacy.language import Language
from traiter.pylib.rules.base import Base as TraiterBase


@dataclass(eq=False)
class Base(TraiterBase):
    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError

    def formatted(self) -> dict[str, str]:
        raise NotImplementedError
