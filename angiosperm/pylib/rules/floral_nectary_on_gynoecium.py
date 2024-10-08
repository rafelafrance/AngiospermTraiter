from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class FloralNectaryOnGynoecium(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "reproductive_type.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, str]:
        return {"Floral nectary on gynoecium": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="floral_nectary_on_gynoecium_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="floral_nectary_on_gynoecium_patterns",
            compiler=cls.floral_nectary_on_gynoecium_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="floral_nectary_on_gynoecium_cleanup")

    @classmethod
    def floral_nectary_on_gynoecium_patterns(cls):
        return [
            Compiler(
                label="floral_nectary_on_gynoecium",
                on_match="floral_nectary_on_gynoecium_match",
                keep="floral_nectary_on_gynoecium",
                decoder={
                    "fill": {"POS": {"IN": ["ADP", "DET"]}},
                    "nectary": {"ENT_TYPE": "floral_nectary_term"},
                    "organ": {"ENT_TYPE": "gynoecium_term"},
                    "secretion": {"ENT_TYPE": "nectar_secretion_term"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " missing* nectary+   fill? fill? organ+ missing* ",
                    " missing* secretion+ fill? fill? organ+ missing* ",
                ],
            ),
        ]

    @classmethod
    def floral_nectary_on_gynoecium_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("floral_nectary_on_gynoecium_match")
def floral_nectary_on_gynoecium_match(ent):
    return FloralNectaryOnGynoecium.floral_nectary_on_gynoecium_match(ent)