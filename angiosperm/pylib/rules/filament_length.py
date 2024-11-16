from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class FilamentLength(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "androecium.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    length: str = None

    def formatted(self) -> dict[str, str]:
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
        length = next(
            (e.text.lower() for e in ent.ents if e.label_ == "filament_length_term"),
            None,
        )
        length = cls.replace.get(length, length)
        return cls.from_ent(ent, length=length)


@registry.misc("filament_length_match")
def filament_length_match(ent):
    return FilamentLength.filament_length_match(ent)
