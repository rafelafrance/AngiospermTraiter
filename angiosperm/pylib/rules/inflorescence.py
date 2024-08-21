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
class Inflorescence(Base):
    # Class vars ----------
    inflorescence_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "inflorescence.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(
        inflorescence_csv, "replace"
    )
    growth: ClassVar[dict[str, str]] = term_util.look_up_table(
        inflorescence_csv, "growth"
    )
    # ---------------------

    morphology: str = None
    growth_pattern: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        data = {}

        if self.morphology is not None:
            data["inflorescenceMorphology"] = self.morphology

        if self.growth_pattern is not None:
            data["inflorescenceGrowthPattern"] = self.growth_pattern

        return dwc.add_dyn(**data)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="inflorescence_terms", path=cls.inflorescence_csv)
        add.trait_pipe(
            nlp,
            name="inflorescence_patterns",
            compiler=cls.inflorescence_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="inflorescence_cleanup")

    @classmethod
    def inflorescence_patterns(cls):
        return [
            Compiler(
                label="inflorescence",
                on_match="inflorescence_match",
                keep="inflorescence",
                decoder={
                    "inflorescence": {"ENT_TYPE": "morphology"},
                },
                patterns=[
                    " inflorescence+ ",
                ],
            ),
        ]

    @classmethod
    def inflorescence_match(cls, ent):
        inflorescence = ent.text.lower()
        morphology = cls.replace.get(inflorescence, inflorescence)
        growth = cls.growth.get(inflorescence)
        print(inflorescence, morphology, growth)
        return cls.from_ent(ent, morphology=morphology, growth_pattern=growth)


@registry.misc("inflorescence_match")
def inflorescence_match(ent):
    return Inflorescence.inflorescence_match(ent)
