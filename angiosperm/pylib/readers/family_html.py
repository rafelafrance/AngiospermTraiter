import dataclasses
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from traiter.pylib.rules.base import Base

from angiosperm.pylib.pipelines import (
    androecium,
    general_floral,
    perianth,
    reproductive_type,
)

PIPELINES = {
    "androecium": androecium.build(),
    "floral": general_floral.build(),
    "inflorescence": general_floral.build(),
    "perianth": perianth.build(),
    "reproductive": reproductive_type.build(),
}


@dataclasses.dataclass
class Paragraph:
    text: str
    traits: list[Base] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Page:
    taxon: str
    paragraphs: list[Paragraph] = dataclasses.field(default_factory=list)


def read(input_dir: Path) -> dict[str, Page]:
    pages: dict[str, Page] = {}

    paths = sorted(input_dir.glob("*.htm*"))

    for path in paths:
        with path.open("rb") as in_file:
            raw = in_file.read()

        soup = BeautifulSoup(raw, features="lxml")

        taxon = get_taxon(soup.title.text)

        if taxon in pages:
            sys.exit(f"Duplicate taxon {taxon}")

        paragraphs = get_paragraphs(soup)

        pages[taxon] = Page(taxon=taxon, paragraphs=paragraphs)

    return pages


def get_taxon(text):
    taxon = text.split("-")[-1]
    taxon = taxon.split()[0]
    return taxon


def get_paragraphs(soup):
    paragraphs: list[Paragraph] = []

    for para in soup.find_all("p"):
        traits: list[Base] = []
        text = " ".join(para.text.split())

        first, *_ = text.split(".")
        first = first.lower()

        parsed = False
        for key, pipeline in PIPELINES.items():
            if key in first:
                doc = pipeline(text)
                traits += [e._.trait for e in doc.ents]
                parsed = True

        if parsed:
            paragraphs.append(Paragraph(text=text, traits=traits))

    return paragraphs
