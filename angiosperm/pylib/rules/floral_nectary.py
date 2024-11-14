from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class FloralNectary(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "reproductive_type.csv",
    ]
    presence: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "presence")
    # ---------------------

    present: str = None

    def formatted(self) -> dict[str, str]:
        return {"Floral nectary present": self.present}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="floral_nectary_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="floral_nectary_patterns",
            compiler=cls.floral_nectary_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="floral_nectary_cleanup")

    @classmethod
    def floral_nectary_patterns(cls):
        return [
            Compiler(
                label="floral_nectary",
                on_match="floral_nectary_match",
                keep="floral_nectary",
                decoder={
                    "nectary": {"ENT_TYPE": "floral_nectary_term"},
                    "presence": {"ENT_TYPE": "presence_term"},
                },
                patterns=[
                    " nectary+ presence+ ",
                ],
            ),
        ]

    @classmethod
    def floral_nectary_match(cls, ent):
        present = next(
            cls.presence.get(e.text.lower(), "1")
            for e in ent.ents
            if e.label_ == "presence_term"
        )
        return cls.from_ent(ent, present=present)


@registry.misc("floral_nectary_match")
def floral_nectary_match(ent):
    return FloralNectary.floral_nectary_match(ent)
