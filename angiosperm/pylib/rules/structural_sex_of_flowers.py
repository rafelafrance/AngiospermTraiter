from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class StructuralSexOfFlowers(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "general_floral_characters.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    structural_sex: str = None
    uncertain: bool = None

    def formatted(self) -> dict[str, str]:
        value = self.structural_sex
        value += " ?" if self.uncertain else ""
        return {"Structural sex of flowers": value}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="structural_sex_of_flowers_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="structural_sex_of_flowers_patterns",
            compiler=cls.structural_sex_of_flowers_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="structural_sex_of_flowers_cleanup")

    @classmethod
    def structural_sex_of_flowers_patterns(cls):
        return [
            Compiler(
                label="structural_sex_of_flowers",
                on_match="structural_sex_of_flowers_match",
                keep="structural_sex_of_flowers",
                decoder={
                    "[?]": {"ENT_TYPE": "q_mark"},
                    "structural_sex": {"ENT_TYPE": "structural_sex_of_flowers_term"},
                },
                patterns=[
                    " structural_sex+ ",
                    " structural_sex+ [?]+ ",
                ],
            ),
        ]

    @classmethod
    def structural_sex_of_flowers_match(cls, ent):
        structural_sex = next(
            (
                e.text.lower()
                for e in ent.ents
                if e.label_ == "structural_sex_of_flowers_term"
            ),
            None,
        )
        structural_sex = cls.replace.get(structural_sex, structural_sex)
        uncertain = next((True for e in ent.ents if e.label_ == "q_mark"), None)
        return cls.from_ent(ent, structural_sex=structural_sex, uncertain=uncertain)


@registry.misc("structural_sex_of_flowers_match")
def structural_sex_of_flowers_match(ent):
    return StructuralSexOfFlowers.structural_sex_of_flowers_match(ent)
