from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class SymmetryOfPerianth(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "perianth.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    symmetry: str = None

    def formatted(self) -> dict[str, Any]:
        return {"Symmetry of perianth": self.symmetry}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="symmetry_of_perianth_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="symmetry_of_perianth_patterns",
            compiler=cls.symmetry_of_perianth_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="symmetry_of_perianth_cleanup")

    @classmethod
    def symmetry_of_perianth_patterns(cls):
        return [
            Compiler(
                label="symmetry_of_perianth",
                on_match="symmetry_of_perianth_match",
                keep="symmetry_of_perianth",
                decoder={
                    "symmetry": {"ENT_TYPE": "symmetry_of_perianth_term"},
                },
                patterns=[
                    " symmetry+ ",
                ],
            ),
        ]

    @classmethod
    def symmetry_of_perianth_match(cls, ent):
        term = "symmetry_of_perianth_term"
        symmetry = next(
            (e.text.lower() for e in ent.ents if e.label_ == term),
            None,
        )
        symmetry = cls.replace.get(symmetry, symmetry)
        return cls.from_ent(ent, symmetry=symmetry)


@registry.misc("symmetry_of_perianth_match")
def symmetry_of_perianth_match(ent):
    return SymmetryOfPerianth.symmetry_of_perianth_match(ent)
