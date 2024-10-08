from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PerianthPresence(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "perianth.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, str]:
        return {"Perianth presence": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="perianth_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="perianth_patterns",
            compiler=cls.perianth_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="perianth_cleanup")

    @classmethod
    def perianth_patterns(cls):
        return [
            Compiler(
                label="perianth",
                on_match="perianth_match",
                keep="perianth",
                decoder={
                    "perianth": {"ENT_TYPE": "perianth_term"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " missing* perianth+ missing* ",
                ],
            ),
        ]

    @classmethod
    def perianth_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("perianth_match")
def perianth_match(ent):
    return PerianthPresence.perianth_match(ent)
