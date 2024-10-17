from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class AndroeciumStructuralPhyllotaxy(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "androecium.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    phyllotaxy: str = None

    def formatted(self) -> dict[str, Any]:
        return {"Androecium structural phyllotaxy": self.phyllotaxy}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(
            nlp, name="androecium_structural_phyllotaxy_terms", path=cls.term_csv
        )
        add.trait_pipe(
            nlp,
            name="androecium_structural_phyllotaxy_patterns",
            compiler=cls.androecium_structural_phyllotaxy_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="androecium_structural_phyllotaxy_cleanup")

    @classmethod
    def androecium_structural_phyllotaxy_patterns(cls):
        return [
            Compiler(
                label="androecium_structural_phyllotaxy",
                on_match="androecium_structural_phyllotaxy_match",
                keep="androecium_structural_phyllotaxy",
                decoder={
                    "phyllotaxy": {"ENT_TYPE": "androecium_structural_phyllotaxy_term"},
                },
                patterns=[
                    " phyllotaxy+ ",
                ],
            ),
        ]

    @classmethod
    def androecium_structural_phyllotaxy_match(cls, ent):
        term = "androecium_structural_phyllotaxy_term"
        phyllotaxy = next(
            (e.text.lower() for e in ent.ents if e.label_ == term),
            None,
        )
        phyllotaxy = cls.replace.get(phyllotaxy, phyllotaxy)
        return cls.from_ent(ent, phyllotaxy=phyllotaxy)


@registry.misc("androecium_structural_phyllotaxy_match")
def androecium_structural_phyllotaxy_match(ent):
    return AndroeciumStructuralPhyllotaxy.androecium_structural_phyllotaxy_match(ent)
