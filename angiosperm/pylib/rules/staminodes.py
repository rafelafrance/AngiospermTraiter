from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class Staminodes(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "androecium.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, Any]:
        return {"Staminodes": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="staminodes_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="staminodes_patterns",
            compiler=cls.staminodes_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="staminodes_cleanup")

    @classmethod
    def staminodes_patterns(cls):
        return [
            Compiler(
                label="staminodes",
                on_match="staminodes_match",
                keep="staminodes",
                decoder={
                    "staminodes": {"ENT_TYPE": "staminode_term"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " missing* staminodes+ missing* ",
                ],
            ),
        ]

    @classmethod
    def staminodes_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("staminodes_match")
def staminodes_match(ent):
    return Staminodes.staminodes_match(ent)
