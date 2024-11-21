from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from angiosperm.pylib.rules.base import Base


# ######################################################################################
@dataclass(eq=False)
class Phyllotaxy(Base):
    # Class vars ----------
    term_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "phyllotaxy.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(term_csv, "replace")
    structure: ClassVar[str] = ""
    # ---------------------

    phyllotaxy: list[str] = None

    def formatted(self) -> dict[str, str]:
        return {
            f"{self.structure.title()} phyllotaxy": ", ".join(sorted(self.phyllotaxy))
        }

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="phyllotaxy_terms", path=cls.term_csv)
        add.trait_pipe(
            nlp,
            name="phyllotaxy_patterns",
            compiler=cls.phyllotaxy_patterns(),
        )
        # add.debug_tokens(nlp)  # #################################################
        add.cleanup_pipe(nlp, name="phyllotaxy_cleanup")

    @classmethod
    def phyllotaxy_patterns(cls):
        return [
            Compiler(
                label=f"{cls.structure}_phyllotaxy",
                on_match="phyllotaxy_match",
                keep=f"{cls.structure}_phyllotaxy",
                decoder={
                    "phyllotaxy": {"ENT_TYPE": {"IN": ["whorls_term", "spirals_term"]}},
                },
                patterns=[
                    " phyllotaxy+ ",
                ],
            ),
        ]

    @classmethod
    def phyllotaxy_match(cls, ent):
        phyllotaxy = set()
        for sub_ent in ent.ents:
            if sub_ent.label_ == "whorls_term":
                phyllotaxy.add("0")
            elif sub_ent.label_ == "spirals_term":
                phyllotaxy.add("1")
        return cls.from_ent(ent, phyllotaxy=sorted(phyllotaxy))


@registry.misc("phyllotaxy_match")
def phyllotaxy_match(ent):
    return Phyllotaxy.phyllotaxy_match(ent)


# ######################################################################################
def get_missing_phyllotaxy(traits):
    found = {t._trait for t in traits}

    # Perianth phyllotaxy
    phyllotaxy = []
    if "perianth_phyllotaxy" not in found and "number_of_perianth_whorls" in found:
        phyllotaxy.append("0")

    if "perianth_phyllotaxy" not in found and "number_of_perianth_spirals" in found:
        phyllotaxy.append("1")

    if phyllotaxy:
        traits.append(
            Phyllotaxy(_trait="perianth_phyllotaxy", phyllotaxy=sorted(phyllotaxy))
        )

    # Androecium phyllotaxy
    phyllotaxy = []
    if "androecium_phyllotaxy" not in found and "number_of_androecium_whorls" in found:
        phyllotaxy.append("0")

    if "androecium_phyllotaxy" not in found and "number_of_androecium_spirals" in found:
        phyllotaxy.append("1")

    if phyllotaxy:
        traits.append(
            Phyllotaxy(_trait="androecium_phyllotaxy", phyllotaxy=sorted(phyllotaxy))
        )
