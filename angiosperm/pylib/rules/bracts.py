from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class Bracts(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "general_floral.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, Any]:
        return {"Bracts": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="bract_terms", path=cls.csvs)
        add.trait_pipe(nlp, name="bract_patterns", compiler=cls.bract_patterns())
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="bract_cleanup")

    @classmethod
    def bract_patterns(cls):
        return [
            Compiler(
                label="bract",
                on_match="bract_match",
                keep="bract",
                decoder={
                    "missing": {"ENT_TYPE": "missing"},
                    "bract_present": {"ENT_TYPE": "bract_presence_term"},
                    "bract_term": {"ENT_TYPE": "bract_term"},
                },
                patterns=[
                    " missing* bract_present+ bract_term* missing* ",
                    " missing*                bract_term+ missing* ",
                ],
            ),
        ]

    @classmethod
    def bract_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("bract_match")
def bract_match(ent):
    return Bracts.bract_match(ent)
