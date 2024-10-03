from dataclasses import dataclass

from spacy import Language

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PerianthPresence(Base):
    present: bool = None

    def formatted(self) -> dict[str, str]:
        return {"Perianth presence": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        pass

    @classmethod
    def perianth_presence(cls, *, present):
        return cls.dummy_ent(
            present=present, _trait="perianth_presence", start=0, end=0, _text=""
        )
