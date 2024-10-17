from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PetaloidBracts(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "general_floral.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, Any]:
        return {"Petaloid bracts": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="petaloid_bracts_bracts_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="petaloid_bracts_patterns",
            compiler=cls.petaloid_bracts_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="petaloid_bracts_cleanup")

    @classmethod
    def petaloid_bracts_patterns(cls):
        return [
            Compiler(
                label="petaloid bracts",
                on_match="petaloid_bracts_match",
                keep="petaloid bracts",
                decoder={
                    "missing": {"ENT_TYPE": "missing"},
                    "bract": {"ENT_TYPE": "petaloid_bract_term"},
                },
                patterns=[
                    " missing* bract+ missing* ",
                ],
            ),
        ]

    @classmethod
    def petaloid_bracts_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("petaloid_bracts_match")
def petaloid_bracts_match(ent):
    return PetaloidBracts.petaloid_bracts_match(ent)
