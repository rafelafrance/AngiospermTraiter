from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.const import QUOTE
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class FlowerGrouping(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "general_floral.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    # ---------------------

    grouping: str = None

    def formatted(self) -> dict[str, str]:
        return {"Flower grouping": self.grouping}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="flower_grouping_terms", path=cls.term_csv)
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
                    "flower": {"ENT_TYPE": "flower_term"},
                    "grouping": {"ENT_TYPE": "grouping_term"},
                    "inflorescences": {"ENT_TYPE": "inflorescences_term"},
                    "'": {"TEXT": {"IN": QUOTE}},
                    "verb": {"POS": "VERB"},
                },
                patterns=[
                    " flower* verb? adp? '? grouping+ '? ",
                    " flower* adv? adp? '? grouping+ '? ",
                    " flower* grouping+ verb? adp? '? inflorescences '? ",
                ],
            ),
        ]

    @classmethod
    def flower_grouping_match(cls, ent):
        grouping = next(
            (
                cls.replace.get(e.text.lower())
                for e in ent.ents
                if e.label_ == "grouping_term"
            ),
            None,
        )
        return cls.from_ent(ent, grouping=grouping)


@registry.misc("flower_grouping_match")
def flower_grouping_match(ent):
    return FlowerGrouping.flower_grouping_match(ent)
