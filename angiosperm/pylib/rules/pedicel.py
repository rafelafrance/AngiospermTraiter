from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class Pedicel(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "general_floral_characters.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, str]:
        return {"Pedicel": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="pedicel_terms", path=cls.csvs)
        add.trait_pipe(nlp, name="pedicel_patterns", compiler=cls.pedicel_patterns())
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="pedicel_cleanup")

    @classmethod
    def pedicel_patterns(cls):
        return [
            Compiler(
                label="pedicel",
                on_match="pedicel_match",
                keep="pedicel",
                decoder={
                    "missing": {"ENT_TYPE": {"IN": ["absent", "missing"]}},
                    "pedicel": {"ENT_TYPE": "present"},
                },
                patterns=[
                    " missing* pedicel+ missing* ",
                    " absent+ ",
                ],
            ),
        ]

    @classmethod
    def pedicel_match(cls, ent):
        present = not any(e.label_ in ["absent", "missing"] for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("pedicel_match")
def pedicel_match(ent):
    return Pedicel.pedicel_match(ent)
