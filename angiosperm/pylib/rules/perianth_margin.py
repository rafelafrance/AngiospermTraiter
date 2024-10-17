from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PerianthMargin(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "perianth.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    margin: str = None

    def formatted(self) -> dict[str, Any]:
        return {"Perianth margin": self.margin}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="perianth_margin_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="perianth_margin_patterns",
            compiler=cls.perianth_margin_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="perianth_margin_cleanup")

    @classmethod
    def perianth_margin_patterns(cls):
        return [
            Compiler(
                label="perianth_margin",
                on_match="perianth_margin_match",
                keep="perianth_margin",
                decoder={
                    "margin": {"ENT_TYPE": "perianth_margin_term"},
                },
                patterns=[
                    " margin+ ",
                ],
            ),
        ]

    @classmethod
    def perianth_margin_match(cls, ent):
        term = "perianth_margin_term"
        margin = next(
            (e.text.lower() for e in ent.ents if e.label_ == term),
            None,
        )
        margin = cls.replace.get(margin, margin)
        return cls.from_ent(ent, margin=margin)


@registry.misc("perianth_margin_match")
def perianth_margin_match(ent):
    return PerianthMargin.perianth_margin_match(ent)
