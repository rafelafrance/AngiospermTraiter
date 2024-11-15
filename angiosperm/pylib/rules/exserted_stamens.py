from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class ExsertedStamens(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "androecium.csv",
        Path(__file__).parent / "terms" / "missing_terms.csv",
    ]
    # ---------------------

    present: str = None

    def formatted(self) -> dict[str, str]:
        return {"Exserted stamens": self.present}

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
        missing = any(e.label_ == "missing" for e in ent.ents)
        present = "0" if missing else "1"
        return cls.from_ent(ent, present=present)


@registry.misc("exserted_stamens_match")
def exserted_stamens_match(ent):
    return ExsertedStamens.exserted_stamens_match(ent)
