from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class Bracts(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "general_floral.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    presence: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "presence")
    # ---------------------

    present: str = None

    def formatted(self) -> dict[str, str]:
        return {"Bracts": self.present}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="bract_terms", path=cls.csvs)
        add.trait_pipe(nlp, name="bract_patterns", compiler=cls.bract_patterns())
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="bract_cleanup")

    @classmethod
    def bract_patterns(cls):
        return [
            Compiler(
                label="bract",
                on_match="bract_match",
                keep="bract",
                decoder={
                    "missing": {"ENT_TYPE": "missing"},
                    "bract_present": {"ENT_TYPE": "bract_presence_term"},
                },
                patterns=[
                    " missing* bract_present+ missing* ",
                ],
            ),
        ]

    @classmethod
    def bract_match(cls, ent):
        missing = any(e.label_ == "missing" for e in ent.ents)
        absent = any(cls.presence.get(e.text.lower()) == "0" for e in ent.ents)
        present = "1" if not (missing or absent) else "0"
        return cls.from_ent(ent, present=present)


@registry.misc("bract_match")
def bract_match(ent):
    return Bracts.bract_match(ent)
