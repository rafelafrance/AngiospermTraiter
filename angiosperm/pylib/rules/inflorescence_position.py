from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class InflorescencePosition(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "general_floral.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    growth: ClassVar[dict[str, str]] = term_util.look_up_table(
        term_csv, "inflorescence_growth_pattern"
    )
    # ---------------------

    position: str = None

    def formatted(self) -> dict[str, Any]:
        return {"Inflorescence position": self.position}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="inflorescence_position_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="inflorescence_position_patterns",
            compiler=cls.inflorescence_position_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="inflorescence_position_cleanup")

    @classmethod
    def inflorescence_position_patterns(cls):
        return [
            Compiler(
                label="inflorescence_position",
                on_match="inflorescence_position_match",
                keep="inflorescence_position",
                decoder={
                    "position": {"ENT_TYPE": "inflorescence_position_term"},
                },
                patterns=[
                    " position+ ",
                ],
            ),
        ]

    @classmethod
    def inflorescence_position_match(cls, ent):
        return cls.from_ent(ent, position=ent.text.lower())


@registry.misc("inflorescence_position_match")
def inflorescence_position_match(ent):
    return InflorescencePosition.inflorescence_position_match(ent)
