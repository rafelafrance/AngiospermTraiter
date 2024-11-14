from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class NectarSecretion(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "reproductive_type.csv",
    ]
    # ---------------------

    organs: list[str] = None

    def formatted(self) -> dict[str, str]:
        return {"Nectar secretion from": ", ".join(self.organs)}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="nectar_secretion_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="nectar_secretion_patterns",
            compiler=cls.nectar_secretion_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="nectar_secretion_cleanup")

    @classmethod
    def nectar_secretion_patterns(cls):
        return [
            Compiler(
                label="nectar_secretion",
                on_match="nectar_secretion_match",
                keep="nectar_secretion",
                decoder={
                    "organ": {"ENT_TYPE": "nectary_organ_term"},
                    "secretion": {"ENT_TYPE": "nectar_secretion_term"},
                    "words": {"IS_SENT_START": False},
                },
                patterns=[
                    " secretion+ words* organ ",
                    " secretion+ words* organ words+ organ ",
                    " secretion+ words* organ words+ organ words+ organ ",
                ],
            ),
        ]

    @classmethod
    def nectar_secretion_match(cls, ent):
        organs = sorted(
            e.text.lower() for e in ent.ents if e.label_ == "nectary_organ_term"
        )
        return cls.from_ent(ent, organs=organs)


@registry.misc("nectar_secretion_match")
def nectar_secretion_match(ent):
    return NectarSecretion.nectar_secretion_match(ent)
