from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class OvaryPosition(Base):
    # Class vars ----------
    ovary_position_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "ovary_position.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(
        ovary_position_csv, "replace"
    )
    # ---------------------

    ovary_position: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(ovaryPosition=self.ovary_position)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="ovary_position_terms", path=cls.ovary_position_csv)
        add.trait_pipe(
            nlp, name="ovary_position_patterns", compiler=cls.ovary_position_patterns()
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="ovary_position_cleanup")

    @classmethod
    def ovary_position_patterns(cls):
        return [
            Compiler(
                label="ovary_position",
                on_match="ovary_position_match",
                keep="ovary_position",
                decoder={
                    "ovary_position": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " ovary_position+ ",
                ],
            ),
        ]

    @classmethod
    def ovary_position_match(cls, ent):
        ovary_position = next(
            (e.text.lower() for e in ent.ents if e.label_ == "position"), None
        )
        ovary_position = cls.replace.get(ovary_position, ovary_position)
        return cls.from_ent(ent, ovary_position=ovary_position)


@registry.misc("ovary_position_match")
def ovary_position_match(ent):
    return OvaryPosition.ovary_position_match(ent)
