from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PlantSexualSystem(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "reproductive_type.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    sexual_system: str = None

    def formatted(self) -> dict[str, str]:
        return {"Plant sexual system": self.sexual_system}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="plant_sexual_system_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="plant_sexual_system_patterns",
            compiler=cls.plant_sexual_system_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="plant_sexual_system_cleanup")

    @classmethod
    def plant_sexual_system_patterns(cls):
        return [
            Compiler(
                label="sexual_system",
                on_match="plant_sexual_system_match",
                keep="sexual_system",
                decoder={
                    "sexual_system": {"ENT_TYPE": "plant_sexual_system_term"},
                },
                patterns=[
                    " sexual_system+ ",
                ],
            ),
        ]

    @classmethod
    def plant_sexual_system_match(cls, ent):
        sexual_system = next(
            e.text.lower() for e in ent.ents if e.label_ == "plant_sexual_system_term"
        )
        sexual_system = cls.replace.get(sexual_system, sexual_system)
        return cls.from_ent(ent, sexual_system=sexual_system)


@registry.misc("plant_sexual_system_match")
def plant_sexual_system_match(ent):
    return PlantSexualSystem.plant_sexual_system_match(ent)
