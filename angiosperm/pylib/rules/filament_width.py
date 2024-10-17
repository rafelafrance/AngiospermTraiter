from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class FilamentWidth(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "androecium.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    length: str = None

    def formatted(self) -> dict[str, Any]:
        return {"Filament length": self.length}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="filament_length_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="filament_length_patterns",
            compiler=cls.filament_length_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="filament_length_cleanup")

    @classmethod
    def filament_length_patterns(cls):
        return [
            Compiler(
                label="filament_length",
                on_match="filament_length_match",
                keep="filament_length",
                decoder={
                    "position": {"ENT_TYPE": "filament_length_term"},
                },
                patterns=[
                    " position+ ",
                ],
            ),
        ]

    @classmethod
    def filament_length_match(cls, ent):
        term = "filament_length_term"
        position = next(
            (e.text.lower() for e in ent.ents if e.label_ == term),
            None,
        )
        position = cls.replace.get(position, position)
        return cls.from_ent(ent, position=position)


@registry.misc("filament_length_match")
def filament_length_match(ent):
    return FilamentWidth.filament_length_match(ent)
