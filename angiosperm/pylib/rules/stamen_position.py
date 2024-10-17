from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class StamenPosition(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "androecium.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    position: str = None

    def formatted(self) -> dict[str, Any]:
        return {"Stamen position": self.position}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="stamen_position_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="stamen_position_patterns",
            compiler=cls.stamen_position_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="stamen_position_cleanup")

    @classmethod
    def stamen_position_patterns(cls):
        return [
            Compiler(
                label="stamen_position",
                on_match="stamen_position_match",
                keep="stamen_position",
                decoder={
                    "position": {"ENT_TYPE": "stamen_position_term"},
                },
                patterns=[
                    " position+ ",
                ],
            ),
        ]

    @classmethod
    def stamen_position_match(cls, ent):
        term = "stamen_position_term"
        position = next(
            (e.text.lower() for e in ent.ents if e.label_ == term),
            None,
        )
        position = cls.replace.get(position, position)
        return cls.from_ent(ent, position=position)


@registry.misc("stamen_position_match")
def stamen_position_match(ent):
    return StamenPosition.stamen_position_match(ent)
