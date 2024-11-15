from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class ClawedPetal(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "perianth.csv",
        Path(__file__).parent / "terms" / "missing_terms.csv",
    ]
    presence: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "presence")
    # ---------------------

    present: str = None

    def formatted(self) -> dict[str, str]:
        return {"Clawed petal": self.present}

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
        missing = any(e.label_ == "missing" for e in ent.ents)
        present = "0" if missing else "1"
        return cls.from_ent(ent, present=present)


@registry.misc("clawed_petal_match")
def clawed_petal_match(ent):
    return ClawedPetal.clawed_petal_match(ent)
