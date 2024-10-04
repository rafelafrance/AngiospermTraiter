from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PerianthDifferentiation(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "perianth.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    differentiation: str = None

    def formatted(self) -> dict[str, str]:
        return {"Perianth differentiation": self.differentiation}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="perianth_differentiation_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="perianth_differentiation_patterns",
            compiler=cls.perianth_differentiation_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="perianth_differentiation_cleanup")

    @classmethod
    def perianth_differentiation_patterns(cls):
        return [
            Compiler(
                label="perianth_differentiation",
                on_match="perianth_differentiation_match",
                keep="perianth_differentiation",
                decoder={
                    "differentiation": {"ENT_TYPE": "perianth_differentiation_term"},
                },
                patterns=[
                    " differentiation+ ",
                ],
            ),
        ]

    @classmethod
    def perianth_differentiation_match(cls, ent):
        term = "perianth_differentiation_term"
        differentiation = next(
            (e.text.lower() for e in ent.ents if e.label_ == term),
            None,
        )
        differentiation = cls.replace.get(differentiation, differentiation)
        return cls.from_ent(ent, differentiation=differentiation)


@registry.misc("perianth_differentiation_match")
def perianth_differentiation_match(ent):
    return PerianthDifferentiation.perianth_differentiation_match(ent)
