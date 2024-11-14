from dataclasses import dataclass
from typing import ClassVar

from spacy import Language

from angiosperm.pylib.rules.base import Base


# ###############################################################################
@dataclass(eq=False)
class FloralNectaryOnAndroecium(Base):
    # Class vars ----------
    trait_name: ClassVar[str] = "floral_nectary_on_androecium"
    # ---------------------

    present: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        ...

    def formatted(self) -> dict[str, str]:
        return {"Floral nectary on androecium": self.present}


# ###############################################################################
@dataclass(eq=False)
class FloralNectaryOnGynoecium(Base):
    # Class vars ----------
    trait_name: ClassVar[str] = "floral_nectary_on_gynoecium"
    # ---------------------

    present: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        ...

    def formatted(self) -> dict[str, str]:
        return {"Floral nectary on gynoecium": self.present}


# ###############################################################################
@dataclass(eq=False)
class FloralNectaryOnPerianth(Base):
    # Class vars ----------
    trait_name: ClassVar[str] = "floral_nectary_on_perianth"
    # ---------------------

    present: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        ...

    def formatted(self) -> dict[str, str]:
        return {"Floral nectary on perianth": self.present}


# ###############################################################################
ORGANS = {
    "androecium": FloralNectaryOnAndroecium,
    "gynoecium": FloralNectaryOnGynoecium,
    "perianth": FloralNectaryOnPerianth,
}


def get_nectaries_secretion(traits):
    organs = set()
    present = ""

    for trait in traits:
        if trait._trait == "nectar_secretion":
            organs |= set(trait.organs)

        if trait._trait == "floral_nectary":
            present = trait.present

    for organ, cls in ORGANS.items():
        if organ in organs and present != "":
            traits.append(cls(_trait=cls.trait_name, present=present))

        elif organ in organs and present == "":
            traits.append(cls(_trait=cls.trait_name, present="-"))

        elif organ not in organs and len(organs) > 0:
            traits.append(cls(_trait=cls.trait_name, present="0"))

        elif len(organs) == 0 and present != "":
            traits.append(cls(_trait=cls.trait_name, present="?"))
