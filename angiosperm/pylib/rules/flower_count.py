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
class FlowerCount(Base):
    # Class vars ----------
    flower_csv: ClassVar[list[Path]] = Path(__file__).parent / "terms" / "flower.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(flower_csv, "replace")
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
        add.term_pipe(nlp, name="flower_count_terms", path=cls.flower_csv)
        add.trait_pipe(
            nlp,
            name="flower_count_patterns",
            compiler=cls.flower_count_patterns(),
            overwrite=["range"],
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="flower_count_cleanup")

    @classmethod
    def flower_count_patterns(cls):
        return [
            Compiler(
                label="flower_count",
                on_match="flower_count_match",
                keep="flower_count",
                decoder={
                    "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
                    "99-99": {"ENT_TYPE": "range"},
                    "flower": {"ENT_TYPE": "flower"},
                },
                patterns=[
                    " flower+ 99-99+ ",
                    " 99-99+ -* flower+ ",
                ],
            ),
        ]

    @classmethod
    def flower_count_match(cls, ent):
        kwargs = {}

        for token in ent:
            if token._.flag == "range_data":
                for key in ("min", "low", "high", "max"):
                    if value := getattr(token._.trait, key, None):
                        value = t_util.to_positive_int(value)
                        if value is None:
                            raise reject_match.RejectMatch
                        kwargs[key] = value

            elif token._.term == "number_word":
                value = cls.replace.get(token.lower_, token.lower_)
                kwargs["low"] = t_util.to_positive_int(value)

        return cls.from_ent(ent, **kwargs)


@registry.misc("flower_count_match")
def structural_sex_match(ent):
    return FlowerCount.flower_count_match(ent)
