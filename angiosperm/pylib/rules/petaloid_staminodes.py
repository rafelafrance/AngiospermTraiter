from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PetaloidStaminodes(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "androecium.csv",
        Path(__file__).parent / "terms" / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, str]:
        return {"Petaloid petaloid_staminodes": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="petaloid_staminodes_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="petaloid_staminodes_patterns",
            compiler=cls.petaloid_staminodes_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="petaloid_staminodes_cleanup")

    @classmethod
    def petaloid_staminodes_patterns(cls):
        return [
            Compiler(
                label="petaloid_staminodes",
                on_match="petaloid_staminodes_match",
                keep="petaloid_staminodes",
                decoder={
                    "petaloid_staminodes": {"ENT_TYPE": "petaloid_staminodes_term"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " missing* petaloid_staminodes+ missing* ",
                ],
            ),
        ]

    @classmethod
    def petaloid_staminodes_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("petaloid_staminodes_match")
def petaloid_staminodes_match(ent):
    return PetaloidStaminodes.petaloid_staminodes_match(ent)
