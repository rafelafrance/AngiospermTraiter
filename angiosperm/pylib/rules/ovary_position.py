from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class OvaryPosition(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "general_floral.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    position: str = None

    def formatted(self) -> dict[str, Any]:
        return {"Ovary position": self.position}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="ovary_position_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp, name="ovary_position_patterns", compiler=cls.ovary_position_patterns()
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="ovary_position_cleanup")

    @classmethod
    def ovary_position_patterns(cls):
        return [
            Compiler(
                label="position",
                on_match="ovary_position_match",
                keep="position",
                decoder={
                    "position": {"ENT_TYPE": "ovary_position_term"},
                },
                patterns=[
                    " position+ ",
                ],
            ),
        ]

    @classmethod
    def ovary_position_match(cls, ent):
        position = next(
            (e.text.lower() for e in ent.ents if e.label_ == "ovary_position_term"),
            None,
        )
        position = cls.replace.get(position, position)
        return cls.from_ent(ent, position=position)


@registry.misc("ovary_position_match")
def ovary_position_match(ent):
    return OvaryPosition.ovary_position_match(ent)
