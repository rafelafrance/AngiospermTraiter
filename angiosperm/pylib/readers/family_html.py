import dataclasses
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from traiter.pylib.rules.base import Base

from angiosperm.pylib.pipelines import util


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
        print(path)
        with path.open("rb") as in_file:
            raw = in_file.read()

        soup = BeautifulSoup(raw, features="lxml")

        taxon = soup.title.text

        if taxon in pages:
            sys.exit(f"Duplicate taxon: {taxon}")

        paragraphs = get_paragraphs(soup)

        pages[taxon] = Page(taxon=taxon, paragraphs=paragraphs)

    return pages


def get_paragraphs(soup):
    paragraphs: list[Paragraph] = []

    for para in soup.find_all("p"):
        traits: list[Base] = []
        text = " ".join(para.text.split())

        first_sent, *_ = text.split(".")
        first_sent = first_sent.lower()

        parsed = False
        for pipeline in util.PIPELINES.values():
            if pipeline.pattern in first_sent:
                traits = util.get_traits(pipeline, text)
                parsed = True

        if parsed:
            paragraphs.append(Paragraph(text=text, traits=traits))

    return paragraphs
