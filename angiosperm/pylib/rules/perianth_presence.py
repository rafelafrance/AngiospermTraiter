from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PerianthPresence(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "perianth.csv",
        Path(__file__).parent / "terms" / "missing_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    present: str = None

    def formatted(self) -> dict[str, str]:
        return {"Perianth presence": self.present}

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
        missing = any(e.label_ == "missing" for e in ent.ents)
        present = "0" if missing else "1"
        return cls.from_ent(ent, present=present)


@registry.misc("perianth_match")
def perianth_match(ent):
    return PerianthPresence.perianth_match(ent)
