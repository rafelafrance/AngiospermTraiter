from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class FlowerGrouping(Base):
    # Class vars ----------
    flower_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "flower.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(flower_csv, "replace")
    # ---------------------

    flower_grouping: str = None

    def formatted(self) -> dict[str, str]:
        return {"Flower grouping": self.flower_grouping}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="flower_grouping_terms", path=cls.flower_csv)
        add.trait_pipe(
            nlp,
            name="flower_grouping_patterns",
            compiler=cls.flower_grouping_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="flower_grouping_cleanup")

    @classmethod
    def flower_grouping_patterns(cls):
        return [
            Compiler(
                label="flower_grouping",
                on_match="flower_grouping_match",
                keep="flower_grouping",
                decoder={
                    "adp": {"POS": "ADP"},
                    "adv": {"POS": "ADV"},
                    "cconj": {"POS": "CCONJ"},
                    "flower": {"ENT_TYPE": "flower"},
                    "flower_grouping": {"ENT_TYPE": "grouping"},
                    "'": {"POS": "PUNCT"},
                    "verb": {"POS": "VERB"},
                },
                patterns=[
                    " flower verb? adp? '? flower_grouping+ '? ",
                    " flower       adv? '? flower_grouping+ '? ",
                    " cconj  verb  adp? '? flower_grouping+ '? ",
                ],
            ),
        ]

    @classmethod
    def flower_grouping_match(cls, ent):
        flower_grouping = next(
            (e.text.lower() for e in ent.ents if e.label_ == "grouping"), None
        )
        flower_grouping = cls.replace.get(flower_grouping, flower_grouping)
        return cls.from_ent(ent, flower_grouping=flower_grouping)


@registry.misc("flower_grouping_match")
def flower_grouping_match(ent):
    return FlowerGrouping.flower_grouping_match(ent)
