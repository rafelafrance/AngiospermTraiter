from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class ExtrafloralNectary(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "leaf_anatomy.csv",
        Path(__file__).parent / "terms" / "missing_terms.csv",
    ]
    # ---------------------

    present: str = None

    def formatted(self) -> dict[str, str]:
        return {"Extrafloral nectary": self.present}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="extrafloral_nectary_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="extrafloral_nectary_patterns",
            compiler=cls.extrafloral_nectary_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="extrafloral_nectary_cleanup")

    @classmethod
    def extrafloral_nectary_patterns(cls):
        return [
            Compiler(
                label="extrafloral_nectary",
                on_match="extrafloral_nectary_match",
                keep="extrafloral_nectary",
                decoder={
                    "extra_floral_nectary": {"ENT_TYPE": "extra_floral_nectary_term"},
                },
                patterns=[
                    " extra_floral_nectary+ ",
                ],
            ),
        ]

    @classmethod
    def extrafloral_nectary_match(cls, ent):
        return cls.from_ent(ent, present="1")


@registry.misc("extrafloral_nectary_match")
def extrafloral_nectary_match(ent):
    return ExtrafloralNectary.extrafloral_nectary_match(ent)
