from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class FloralNectaryOnAndroecium(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "general_floral.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, str]:
        return {"Floral nectary on androecium": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="floral_nectary_on_androecium_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="floral_nectary_on_androecium_patterns",
            compiler=cls.floral_nectary_on_androecium_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="floral_nectary_on_androecium_cleanup")

    @classmethod
    def floral_nectary_on_androecium_patterns(cls):
        return [
            Compiler(
                label="floral_nectary_on_androecium",
                on_match="floral_nectary_on_androecium_match",
                keep="floral_nectary_on_androecium",
                decoder={
                    "adp": {"POS": "ADP"},
                    "floral_nectary": {"ENT_TYPE": "floral_nectary_term"},
                    "nectary_position": {"ENT_TYPE": "androecium_term"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " missing* floral_nectary+ adp? nectary_position+ missing* ",
                ],
            ),
        ]

    @classmethod
    def floral_nectary_on_androecium_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("floral_nectary_on_androecium_match")
def floral_nectary_on_androecium_match(ent):
    return FloralNectaryOnAndroecium.floral_nectary_on_androecium_match(ent)
