from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

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

    width: str = None

    def formatted(self) -> dict[str, str]:
        return {"Filament width": self.width}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="filament_width_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="filament_width_patterns",
            compiler=cls.filament_width_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="filament_width_cleanup")

    @classmethod
    def filament_width_patterns(cls):
        return [
            Compiler(
                label="filament_width",
                on_match="filament_width_match",
                keep="filament_width",
                decoder={
                    "position": {"ENT_TYPE": "filament_width_term"},
                },
                patterns=[
                    " position+ ",
                ],
            ),
        ]

    @classmethod
    def filament_width_match(cls, ent):
        width = next(
            (e.text.lower() for e in ent.ents if e.label_ == "filament_width_term"),
            None,
        )
        width = cls.replace.get(width, width)
        return cls.from_ent(ent, width=width)


@registry.misc("filament_width_match")
def filament_width_match(ent):
    return FilamentWidth.filament_width_match(ent)
