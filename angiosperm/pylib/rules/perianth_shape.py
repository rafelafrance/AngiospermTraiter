from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class PerianthShape(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "perianth.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    shape: str = None

    def formatted(self) -> dict[str, str]:
        return {"Perianth shape": self.shape}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="perianth_shape_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="perianth_shape_patterns",
            compiler=cls.perianth_shape_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="perianth_shape_cleanup")

    @classmethod
    def perianth_shape_patterns(cls):
        return [
            Compiler(
                label="perianth_shape",
                on_match="perianth_shape_match",
                keep="perianth_shape",
                decoder={
                    "shape": {"ENT_TYPE": "perianth_shape_term"},
                },
                patterns=[
                    " shape+ ",
                ],
            ),
        ]

    @classmethod
    def perianth_shape_match(cls, ent):
        term = "perianth_shape_term"
        shape = next(
            (e.text.lower() for e in ent.ents if e.label_ == term),
            None,
        )
        shape = cls.replace.get(shape, shape)
        return cls.from_ent(ent, shape=shape)


@registry.misc("perianth_shape_match")
def perianth_shape_match(ent):
    return PerianthShape.perianth_shape_match(ent)
