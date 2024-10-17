from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class ExsertedStamens(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "androecium.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]
    # ---------------------

    present: bool = None

    def formatted(self) -> dict[str, Any]:
        return {"Exserted stamens": "present" if self.present else "absent"}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="exserted_stamens_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="exserted_stamens_patterns",
            compiler=cls.exserted_stamens_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="exserted_stamens_cleanup")

    @classmethod
    def exserted_stamens_patterns(cls):
        return [
            Compiler(
                label="exserted_stamens",
                on_match="exserted_stamens_match",
                keep="exserted_stamens",
                decoder={
                    "exserted_stamens": {"ENT_TYPE": "exserted_stamens_presence"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " missing* exserted_stamens+ missing* ",
                ],
            ),
        ]

    @classmethod
    def exserted_stamens_match(cls, ent):
        present = not any(e.label_ == "missing" for e in ent.ents)
        return cls.from_ent(ent, present=present)


@registry.misc("exserted_stamens_match")
def exserted_stamens_match(ent):
    return ExsertedStamens.exserted_stamens_match(ent)
