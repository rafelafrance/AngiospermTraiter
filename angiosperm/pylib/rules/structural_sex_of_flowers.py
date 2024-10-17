from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class StructuralSexOfFlowers(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "reproductive_type.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    presence: ClassVar[dict[str, str]] = term_util.look_up_table(
        term_csv, "presence", int
    )
    # ---------------------

    structural_sex: int = None

    def formatted(self) -> dict[str, Any]:
        return {"Structural sex of flowers": self.structural_sex}

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
                    "structural_sex": {"ENT_TYPE": "structural_sex_of_flowers_term"},
                },
                patterns=[
                    " structural_sex+ ",
                ],
            ),
        ]

    @classmethod
    def structural_sex_of_flowers_match(cls, ent):
        structural_sex = cls.presence.get(ent.text.lower())
        return cls.from_ent(ent, structural_sex=structural_sex)


@registry.misc("structural_sex_of_flowers_match")
def structural_sex_of_flowers_match(ent):
    return StructuralSexOfFlowers.structural_sex_of_flowers_match(ent)
