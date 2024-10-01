from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class Bract(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "general_floral_characters.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, str]:
        label = "Petaloid bracts" if self._trait == "petaloid_bracts" else "Bracts"
        return {label: "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="bract_terms", path=cls.csvs)
        add.trait_pipe(nlp, name="petaloid_patterns", compiler=cls.petaloid_patterns())
        add.trait_pipe(nlp, name="bract_patterns", compiler=cls.bract_patterns())
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="bract_cleanup")

    @classmethod
    def petaloid_patterns(cls):
        return [
            Compiler(
                label="petaloid_bracts",
                on_match="petaloid_match",
                keep="petaloid_bracts",
                decoder={
                    "petaloid": {"ENT_TYPE": "petaloid_bracts"},
                },
                patterns=[
                    " petaloid* ",
                ],
            ),
        ]

    @classmethod
    def bract_patterns(cls):
        return [
            Compiler(
                label="bract",
                on_match="bract_match",
                keep="bract",
                decoder={
                    "missing": {"ENT_TYPE": "missing"},
                    "bract": {"ENT_TYPE": "present"},
                },
                patterns=[
                    " missing* bract+ missing* ",
                ],
            ),
        ]

    @classmethod
    def petaloid_match(cls, ent):
        return cls.from_ent(ent, present=True)

    @classmethod
    def bract_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("petaloid_match")
def petaloid_match(ent):
    return Bract.petaloid_match(ent)


@registry.misc("bract_match")
def bract_match(ent):
    return Bract.bract_match(ent)
