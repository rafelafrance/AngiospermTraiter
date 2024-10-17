from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class ClawedPetal(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "perianth.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, Any]:
        return {"Clawed petal": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="clawed_petal_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="clawed_petal_patterns",
            compiler=cls.clawed_petal_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="clawed_petal_cleanup")

    @classmethod
    def clawed_petal_patterns(cls):
        return [
            Compiler(
                label="clawed_petal",
                on_match="clawed_petal_match",
                keep="clawed_petal",
                decoder={
                    "clawed": {"ENT_TYPE": "clawed_petal_term"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " missing* clawed+ missing* ",
                ],
            ),
        ]

    @classmethod
    def clawed_petal_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("clawed_petal_match")
def clawed_petal_match(ent):
    return ClawedPetal.clawed_petal_match(ent)
