from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PerianthPhyllotaxy(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "perianth.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    phyllotaxy: list[str] = None

    def formatted(self) -> dict[str, str]:
        return {"Perianth phyllotaxy": ", ".join(sorted(self.phyllotaxy))}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="perianth_phyllotaxy_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="perianth_phyllotaxy_patterns",
            compiler=cls.perianth_phyllotaxy_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="perianth_phyllotaxy_cleanup")

    @classmethod
    def perianth_phyllotaxy_patterns(cls):
        return [
            Compiler(
                label="perianth_phyllotaxy",
                on_match="perianth_phyllotaxy_match",
                keep="perianth_phyllotaxy",
                decoder={
                    "phyllotaxy": {"ENT_TYPE": {"IN": ["whorls_term", "spirals_term"]}},
                },
                patterns=[
                    " phyllotaxy+ ",
                ],
            ),
        ]

    @classmethod
    def perianth_phyllotaxy_match(cls, ent):
        phyllotaxy = [
            cls.replace[e.text.lower()]
            for e in ent.ents
            if ent.label_ in ["whorls_term", "spirals_term"]
        ]
        return cls.from_ent(ent, phyllotaxy=phyllotaxy)


@registry.misc("perianth_phyllotaxy_match")
def perianth_phyllotaxy_match(ent):
    return PerianthPhyllotaxy.perianth_phyllotaxy_match(ent)
