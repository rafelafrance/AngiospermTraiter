from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PerianthMerism(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "perianth.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    merism: str = None

    def formatted(self) -> dict[str, Any]:
        return {"Perianth merism": self.merism}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="perianth_merism_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="perianth_merism_patterns",
            compiler=cls.perianth_merism_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="perianth_merism_cleanup")

    @classmethod
    def perianth_merism_patterns(cls):
        return [
            Compiler(
                label="perianth_merism",
                on_match="perianth_merism_match",
                keep="perianth_merism",
                decoder={
                    "merism": {"ENT_TYPE": "perianth_merism_term"},
                },
                patterns=[
                    " merism+ ",
                ],
            ),
        ]

    @classmethod
    def perianth_merism_match(cls, ent):
        term = "perianth_merism_term"
        merism = next(
            (e.text.lower() for e in ent.ents if e.label_ == term),
            None,
        )
        merism = cls.replace.get(merism, merism)
        return cls.from_ent(ent, merism=merism)


@registry.misc("perianth_merism_match")
def perianth_merism_match(ent):
    return PerianthMerism.perianth_merism_match(ent)
