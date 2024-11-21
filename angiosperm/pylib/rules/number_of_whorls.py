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
class NumberOfWhorls(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "phyllotaxy.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    structure: ClassVar[str] = "<Not set>"
    # ---------------------

    min: int = None
    low: int = None
    high: int = None
    max: int = None

    def formatted(self) -> dict[str, str]:
        value = [
            f"{k}={v}"
            for k in ("min", "low", "high", "max")
            if (v := getattr(self, k)) is not None
        ]
        value = ", ".join(value)
        return {f"Number of {self.structure} whorls": value}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="number_of_whorls_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="number_of_whorls_patterns",
            compiler=cls.number_of_whorls_patterns(),
            overwrite=["range"],
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="number_of_whorls_cleanup")

    @classmethod
    def number_of_whorls_patterns(cls):
        return [
            Compiler(
                label=f"number_of_{cls.structure}_whorls",
                on_match="number_of_whorls_match",
                keep=f"number_of_{cls.structure}_whorls",
                decoder={
                    "-": {"TEXT": {"IN": t_const.DASH}},
                    "99-99": {"ENT_TYPE": "range"},
                    "whorls": {"ENT_TYPE": "whorls_term"},
                    "count": {"ENT_TYPE": "whorl_count_term"},
                },
                patterns=[
                    " whorls+ 99-99+ ",
                    " 99-99+ -* whorls+ ",
                    " count ",
                ],
            ),
        ]

    @classmethod
    def number_of_whorls_match(cls, ent):
        kwargs = {}

        for token in ent:
            if token._.flag == "range_data":
                for key in ("min", "low", "high", "max"):
                    if value := getattr(token._.trait, key, None):
                        value = t_util.to_positive_int(value)
                        if value is None:
                            raise reject_match.RejectMatch
                        kwargs[key] = value

            elif token._.term == "whorl_count_term":
                value = cls.replace.get(token.lower_, token.lower_)
                kwargs["low"] = t_util.to_positive_int(value)

        if not kwargs:
            raise reject_match.RejectMatch

        return cls.from_ent(ent, **kwargs)


@registry.misc("number_of_whorls_match")
def number_of_whorls_match(ent):
    return NumberOfWhorls.number_of_whorls_match(ent)
