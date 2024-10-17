from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class RelativeLengthsOfStamens(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "androecium.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    length: str = None

    def formatted(self) -> dict[str, Any]:
        return {"Relative lengths of stamens": self.length}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="relative_lengths_of_stamens_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="relative_lengths_of_stamens_patterns",
            compiler=cls.relative_lengths_of_stamens_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="relative_lengths_of_stamens_cleanup")

    @classmethod
    def relative_lengths_of_stamens_patterns(cls):
        return [
            Compiler(
                label="relative_lengths_of_stamens",
                on_match="relative_lengths_of_stamens_match",
                keep="relative_lengths_of_stamens",
                decoder={
                    "length": {"ENT_TYPE": "relative_lengths_of_stamens_term"},
                },
                patterns=[
                    " length+ ",
                ],
            ),
        ]

    @classmethod
    def relative_lengths_of_stamens_match(cls, ent):
        term = "relative_lengths_of_stamens_term"
        length = next(
            (e.text.lower() for e in ent.ents if e.label_ == term),
            None,
        )
        length = cls.replace.get(length, length)
        return cls.from_ent(ent, length=length)


@registry.misc("relative_lengths_of_stamens_match")
def relative_lengths_of_stamens_match(ent):
    return RelativeLengthsOfStamens.relative_lengths_of_stamens_match(ent)
