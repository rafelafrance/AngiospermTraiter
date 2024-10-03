from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib import util as t_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class NumberOfFertileStamens(Base):
    # Class vars ----------
    term_csv: ClassVar[list[Path]] = Path(__file__).parent / "terms" / "androecium.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    min: int = None
    low: int = None
    high: int = None
    max: int = None

    def formatted(self) -> dict[str, str]:
        value = [
            f"{k}={v}"
            for k in ("min", "low", "high", "max")
            if (v := getattr(self, k) is not None)
        ]
        value = ", ".join(value)
        return {"Number of flowers in an inflorescence": value}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="number_of_fertile_stamens_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="number_of_fertile_stamens_patterns",
            compiler=cls.number_of_fertile_stamens_patterns(),
            overwrite=["range"],
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="number_of_fertile_stamens_cleanup")

    @classmethod
    def number_of_fertile_stamens_patterns(cls):
        return [
            Compiler(
                label="number_of_fertile_stamens",
                on_match="number_of_fertile_stamens_match",
                keep="number_of_fertile_stamens",
                decoder={
                    "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
                    "99-99": {"ENT_TYPE": "range"},
                    "fertile_stamens": {"ENT_TYPE": "fertile_stamens_term"},
                },
                patterns=[
                    " fertile_stamens+ 99-99+ ",
                    " 99-99+ -* fertile_stamens+ ",
                ],
            ),
        ]

    @classmethod
    def number_of_fertile_stamens_match(cls, ent):
        kwargs = {}

        for token in ent:
            if token._.flag == "range_data":
                for key in ("min", "low", "high", "max"):
                    if value := getattr(token._.trait, key, None):
                        value = t_util.to_positive_int(value)
                        if value is None:
                            raise reject_match.RejectMatch
                        kwargs[key] = value

            elif token._.term == "number_term":
                value = cls.replace.get(token.lower_, token.lower_)
                kwargs["low"] = t_util.to_positive_int(value)

        return cls.from_ent(ent, **kwargs)


@registry.misc("number_of_fertile_stamens_match")
def number_of_fertile_stamens_match(ent):
    return NumberOfFertileStamens.number_of_fertile_stamens_match(ent)
