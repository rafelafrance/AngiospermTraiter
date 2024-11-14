from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class Pedicel(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "general_floral.csv",
        Path(__file__).parent / "terms" / "missing_terms.csv",
    ]
    presence: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "presence")
    # ---------------------

    present: str = None

    def formatted(self) -> dict[str, str]:
        return {"Pedicel": self.present}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="pedicel_terms", path=cls.csvs)
        add.trait_pipe(nlp, name="pedicel_patterns", compiler=cls.pedicel_patterns())
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="pedicel_cleanup")

    @classmethod
    def pedicel_patterns(cls):
        return [
            Compiler(
                label="pedicel",
                on_match="pedicel_match",
                keep="pedicel",
                decoder={
                    "pedicel_present": {"ENT_TYPE": "pedicel_presence"},
                },
                patterns=[
                    " pedicel_present+ ",
                ],
            ),
        ]

    @classmethod
    def pedicel_match(cls, ent):
        pedicel = ent.text.lower()
        present_ = cls.presence.get(pedicel, "1")
        return cls.from_ent(ent, present=present_)


@registry.misc("pedicel_match")
def pedicel_match(ent):
    return Pedicel.pedicel_match(ent)
