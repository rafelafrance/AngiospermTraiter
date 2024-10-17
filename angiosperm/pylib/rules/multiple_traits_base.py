"""
A single pattern can match multiple traits.

There are situations where I need a single pattern to match multiple traits.
This is most common when traits are intertwined. For instance, given:
Androecium 2–5, or 8, or 10, or 20–60
I want to pull out 4 separate fertile stamen counts.
"""  # noqa: RUF002

from dataclasses import dataclass
from typing import Any

from spacy.language import Language
from traiter.pylib.darwin_core import DarwinCore

from angiosperm.pylib.rules.base import Base


@dataclass(eq=False)
class MultipleTraitsBase(Base):
    _start_token: int = None
    _end_token: int = None

    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError

    def formatted(self) -> dict[str, Any]:
        raise NotImplementedError

    def to_dwc(self, dwc) -> DarwinCore:
        ...
