from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class FusionToInnerPerianth(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "perianth.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    fusion: str = None

    def formatted(self) -> dict[str, str]:
        return {"Fusion of filaments to inner perianth": self.fusion}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="fusion_to_inner_perianth_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="fusion_to_inner_perianth_patterns",
            compiler=cls.fusion_to_inner_perianth_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="fusion_to_inner_perianth_cleanup")

    @classmethod
    def fusion_to_inner_perianth_patterns(cls):
        return [
            Compiler(
                label="fusion_to_inner_perianth",
                on_match="fusion_to_inner_perianth_match",
                keep="fusion_to_inner_perianth",
                decoder={
                    "fusion": {"ENT_TYPE": "fusion_to_inner_perianth_term"},
                },
                patterns=[
                    " fusion+ ",
                ],
            ),
        ]

    @classmethod
    def fusion_to_inner_perianth_match(cls, ent):
        fusion = next(
            (
                e.text.lower()
                for e in ent.ents
                if e.label_ == "fusion_to_inner_perianth_term"
            ),
            None,
        )
        fusion = cls.replace.get(fusion, fusion)
        return cls.from_ent(ent, fusion=fusion)


@registry.misc("fusion_to_inner_perianth_match")
def fusion_to_inner_perianth_match(ent):
    return FusionToInnerPerianth.fusion_to_inner_perianth_match(ent)
