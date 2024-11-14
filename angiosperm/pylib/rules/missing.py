from angiosperm.pylib.rules.bracts import Bracts
from angiosperm.pylib.rules.petaloid_bracts import PetaloidBracts

MISSING = {
    "bracts": Bracts,
    "petaloid_bracts": PetaloidBracts,
}


def get_missing(traits):
    found = {t._trait for t in traits}
    for trait_name, cls in MISSING.items():
        if trait_name not in found:
            trait = cls(_trait=trait_name, present="?")
            traits.append(trait)
