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
    _start_token: int = None
    _end_token: int = None

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
                    ",": {"POS": "PUNCT"},
                    "or": {"POS": "CCONJ"},
                    "androecium": {"ENT_TYPE": "androecium_term"},
                },
                patterns=[
                    " androecium+ 99-99+ ",
                    " androecium+ 99-99+ ,? or 99-99+ ",
                ],
            ),
        ]

    @classmethod
    def number_of_fertile_stamens_match(cls, ent):
        """WARNING: Adding multiple traits."""
        all_traits = []

        for sub_ent in ent.ents:
            if sub_ent.label_ == "range":
                kwargs = {
                    "_start_token": sub_ent.start,
                    "_end_token": sub_ent.end,
                }
                token = ent[sub_ent.start]

                for key in ("min", "low", "high", "max"):
                    if value := getattr(token._.trait, key, None):
                        value = t_util.to_positive_int(value)
                        if value is None:
                            raise reject_match.RejectMatch
                        kwargs[key] = value

                    elif token._.term == "number_term":
                        value = cls.replace.get(token.lower_, token.lower_)
                        kwargs["low"] = t_util.to_positive_int(value)

                first = len(all_traits) == 0
                start_char = ent.start_char if first else sub_ent.start_char
                end_char = sub_ent.end_char
                all_traits.append(
                    NumberOfFertileStamens(
                        start=start_char,
                        end=end_char,
                        _trait="number_of_fertile_stamens",
                        _text=ent.text[start_char:end_char],
                        **kwargs,
                    )
                )

        return all_traits


@registry.misc("number_of_fertile_stamens_match")
def number_of_fertile_stamens_match(ent):
    return NumberOfFertileStamens.number_of_fertile_stamens_match(ent)
