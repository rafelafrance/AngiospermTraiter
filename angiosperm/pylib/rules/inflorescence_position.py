from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class InflorescencePosition(Base):
    # Class vars ----------
    inflorescence_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "inflorescence.csv"
    )
    # ---------------------

    position: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(inflorescencePosition=self.position)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(
            nlp, name="inflorescence_position_terms", path=cls.inflorescence_csv
        )
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
                    "position": {"ENT_TYPE": "position"},
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
