from dataclasses import dataclass
from typing import ClassVar

from angiosperm.pylib.rules.bracts import Bracts
from angiosperm.pylib.rules.extrafloral_nectary import ExtrafloralNectary
from angiosperm.pylib.rules.petaloid_bracts import PetaloidBracts


@dataclass
class MissingBracts:
    # Class vars ----------
    paragraph: ClassVar[str] = "general_floral"
    # ---------------------
    cls = Bracts
    when_missing = "?"


@dataclass
class MissingPetaloidBracts:
    # Class vars ----------
    paragraph: ClassVar[str] = "general_floral"
    # ---------------------
    cls = PetaloidBracts
    when_missing = "?"


@dataclass
class MissingExtrafloralNectary:
    # Class vars ----------
    paragraph: ClassVar[str] = "leaf_anatomy"
    # ---------------------
    cls = ExtrafloralNectary
    when_missing = "0"


MISSING = {
    "bracts": MissingBracts,
    "petaloid_bracts": MissingPetaloidBracts,
    "extrafloral_nectary": MissingExtrafloralNectary,
}


def get_missing(traits):
    found = {t._trait for t in traits}
    for trait_name, missing in MISSING.items():
        if trait_name not in found:
            trait = missing.cls(
                present=missing.when_missing,
                _trait=trait_name,
                _paragraph=missing.paragraph,
            )
            traits.append(trait)
