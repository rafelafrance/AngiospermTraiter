from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class FusionOfFilaments(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "androecium.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    fusion: str = None

    def formatted(self) -> dict[str, Any]:
        return {"Fusion of filaments": self.fusion}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="fusion_of_filaments_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="fusion_of_filaments_patterns",
            compiler=cls.fusion_of_filaments_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="fusion_of_filaments_cleanup")

    @classmethod
    def fusion_of_filaments_patterns(cls):
        return [
            Compiler(
                label="fusion_of_filaments",
                on_match="fusion_of_filaments_match",
                keep="fusion_of_filaments",
                decoder={
                    "fusion": {"ENT_TYPE": "fusion_of_filaments_term"},
                },
                patterns=[
                    " fusion+ ",
                ],
            ),
        ]

    @classmethod
    def fusion_of_filaments_match(cls, ent):
        fusion = next(
            (
                e.text.lower()
                for e in ent.ents
                if e.label_ == "fusion_of_filaments_term"
            ),
            None,
        )
        fusion = cls.replace.get(fusion, fusion)
        return cls.from_ent(ent, fusion=fusion)


@registry.misc("fusion_of_filaments_match")
def fusion_of_filaments_match(ent):
    return FusionOfFilaments.fusion_of_filaments_match(ent)
