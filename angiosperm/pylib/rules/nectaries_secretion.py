from dataclasses import dataclass
from typing import ClassVar

from spacy import Language

from angiosperm.pylib.rules.base import Base


# ###############################################################################
@dataclass(eq=False)
class FloralNectaryOnAndroecium(Base):
    # Class vars ----------
    trait_name: ClassVar[str] = "floral_nectary_on_androecium"
    paragraph: ClassVar[str] = "reproductive_type"
    # ---------------------

    present: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        ...

    def formatted(self) -> dict[str, str]:
        return {"Floral nectary on androecium ": self.present}


# ###############################################################################
@dataclass(eq=False)
class FloralNectaryOnGynoecium(Base):
    # Class vars ----------
    trait_name: ClassVar[str] = "floral_nectary_on_gynoecium"
    paragraph: ClassVar[str] = "reproductive_type"
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
    paragraph: ClassVar[str] = "reproductive_type"
    # ---------------------

    present: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        ...

    def formatted(self) -> dict[str, str]:
        return {"Floral nectary on perianth ": self.present}


# ###############################################################################
NECTARY_TYPE = [
    FloralNectaryOnAndroecium | FloralNectaryOnGynoecium | FloralNectaryOnPerianth
]
ORGANS: dict[str, NECTARY_TYPE] = {
    "androecium": FloralNectaryOnAndroecium,
    "gynoecium": FloralNectaryOnGynoecium,
    "perianth": FloralNectaryOnPerianth,
}


# ###############################################################################
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
            traits.append(
                cls(_trait=cls.trait_name, present=present, _paragraph=cls.paragraph)
            )

        elif organ not in organs and len(organs) > 0:
            traits.append(
                cls(_trait=cls.trait_name, present="0", _paragraph=cls.paragraph)
            )

        elif present != "1":
            traits.append(
                cls(_trait=cls.trait_name, present="-", _paragraph=cls.paragraph)
            )

        elif present == "1":
            traits.append(
                cls(_trait=cls.trait_name, present="?", _paragraph=cls.paragraph)
            )
