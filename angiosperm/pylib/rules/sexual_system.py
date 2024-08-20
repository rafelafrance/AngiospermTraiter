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
class SexualSystem(Base):
    # Class vars ----------
    sexual_system_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "sexual_system.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(
        sexual_system_csv, "replace"
    )
    # ---------------------

    sexual_system: str = None
    uncertain: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(plantSexualSystem=self.sexual_system)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="sexual_system_terms", path=cls.sexual_system_csv)
        add.trait_pipe(
            nlp, name="sexual_system_patterns", compiler=cls.sexual_system_patterns()
        )
        add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="sexual_system_cleanup")

    @classmethod
    def sexual_system_patterns(cls):
        return [
            Compiler(
                label="sexual_system",
                on_match="sexual_system_match",
                keep="sexual_system",
                decoder={
                    "[?]": {"ENT_TYPE": "q_mark"},
                    "sexual_system": {"ENT_TYPE": "system"},
                },
                patterns=[
                    " sexual_system+ ",
                    " sexual_system+ [?]+ ",
                ],
            ),
        ]

    @classmethod
    def sexual_system_match(cls, ent):
        sexual_system = next(
            (e.text.lower() for e in ent.ents if e.label_ == "system"), None
        )
        sexual_system = cls.replace.get(sexual_system, sexual_system)
        uncertain = next((True for e in ent.ents if e.label_ == "q_mark"), None)
        return cls.from_ent(ent, sexual_system=sexual_system, uncertain=uncertain)


@registry.misc("sexual_system_match")
def sexual_system_match(ent):
    return SexualSystem.sexual_system_match(ent)
