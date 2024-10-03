from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class InflorescenceMorphology(Base):
    # Class vars ----------
    inflorescence_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "general_floral_characters.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(
        inflorescence_csv, "replace"
    )
    growth: ClassVar[dict[str, str]] = term_util.look_up_table(
        inflorescence_csv, "inflorescence_growth_pattern"
    )
    # ---------------------

    morphology: str = None
    growth_pattern: str = None

    def formatted(self) -> dict[str, str]:
        data = {}

        if self.morphology is not None:
            data["Inflorescence morphology"] = self.morphology

        if self.growth_pattern is not None:
            data["Inflorescence growth pattern"] = self.growth_pattern

        return data

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(
            nlp, name="inflorescence_morphology_terms", path=cls.inflorescence_csv
        )
        add.trait_pipe(
            nlp,
            name="inflorescence_morphology_patterns",
            compiler=cls.inflorescence_morphology_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="inflorescence_morphology_cleanup")

    @classmethod
    def inflorescence_morphology_patterns(cls):
        return [
            Compiler(
                label="inflorescence_morphology",
                on_match="inflorescence_morphology_match",
                keep="inflorescence_morphology",
                decoder={
                    "morphology": {"ENT_TYPE": "inflorescence_morphology_term"},
                },
                patterns=[
                    " morphology+ ",
                ],
            ),
        ]

    @classmethod
    def inflorescence_morphology_match(cls, ent):
        morphology = ent.text.lower()
        morphology = cls.replace.get(morphology, morphology)
        growth = cls.growth.get(morphology)
        return cls.from_ent(ent, morphology=morphology, growth_pattern=growth)


@registry.misc("inflorescence_morphology_match")
def inflorescence_morphology_match(ent):
    return InflorescenceMorphology.inflorescence_morphology_match(ent)
