from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class SaccatePerianth(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "perianth.csv",
        Path(__file__).parent / "terms" / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, str]:
        return {"Saccate perianth": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="saccate_perianth_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="saccate_perianth_patterns",
            compiler=cls.saccate_perianth_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="saccate_perianth_cleanup")

    @classmethod
    def saccate_perianth_patterns(cls):
        return [
            Compiler(
                label="saccate_perianth",
                on_match="saccate_perianth_match",
                keep="saccate_perianth",
                decoder={
                    "saccate": {"ENT_TYPE": "saccate_term"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " missing* saccate+ missing* ",
                ],
            ),
        ]

    @classmethod
    def saccate_perianth_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("saccate_perianth_match")
def saccate_perianth_match(ent):
    return SaccatePerianth.saccate_perianth_match(ent)
