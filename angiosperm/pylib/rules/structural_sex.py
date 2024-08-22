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
class StructuralSex(Base):
    # Class vars ----------
    sex_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "sex.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(sex_csv, "replace")
    # ---------------------

    structural_sex: str = None
    uncertain: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add(structuralSexOfFlowers=self.structural_sex)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="structural_sex_terms", path=cls.sex_csv)
        add.trait_pipe(
            nlp, name="structural_sex_patterns", compiler=cls.structural_sex_patterns()
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="structural_sex_cleanup")

    @classmethod
    def structural_sex_patterns(cls):
        return [
            Compiler(
                label="structural_sex",
                on_match="structural_sex_match",
                keep="structural_sex",
                decoder={
                    "[?]": {"ENT_TYPE": "q_mark"},
                    "structural_sex": {"ENT_TYPE": "structural"},
                },
                patterns=[
                    " structural_sex+ ",
                    " structural_sex+ [?]+ ",
                ],
            ),
        ]

    @classmethod
    def structural_sex_match(cls, ent):
        structural_sex = next(
            (e.text.lower() for e in ent.ents if e.label_ == "structural"), None
        )
        structural_sex = cls.replace.get(structural_sex, structural_sex)
        uncertain = next((True for e in ent.ents if e.label_ == "q_mark"), None)
        return cls.from_ent(ent, structural_sex=structural_sex, uncertain=uncertain)


@registry.misc("structural_sex_match")
def structural_sex_match(ent):
    return StructuralSex.structural_sex_match(ent)
