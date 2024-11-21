import dataclasses
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from tqdm import tqdm

from angiosperm.pylib.pipelines import util
from angiosperm.pylib.rules import missing, nectaries_secretion, phyllotaxy
from angiosperm.pylib.rules.base import Base


@dataclasses.dataclass
class Paragraph:
    label: str
    text: str
    traits: list[Base] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Page:
    taxon: str
    paragraphs: dict[str, Paragraph] = dataclasses.field(default_factory=dict)

    @property
    def all_traits(self) -> list[Base]:
        traits: list[Base] = []
        for para in self.paragraphs.values():
            traits += para.traits
        return traits


def read(input_dir: Path, limit: int = 0) -> dict[str, Page]:
    pages: dict[str, Page] = {}

    paths = [p for p in sorted(input_dir.glob("*.htm*")) if p.stem != "chars"]
    if limit > 0:
        paths = paths[:limit]

    for path in tqdm(paths):
        with path.open("rb") as in_file:
            raw = in_file.read()

        soup = BeautifulSoup(raw, features="lxml")

        taxon = soup.title.text
        taxon = re.sub(r"^.*?-\s*", "", taxon).strip()

        if taxon in pages:
            sys.exit(f"Duplicate taxon: {taxon}")

        paragraphs = get_paragraphs(soup)

        pages[taxon] = Page(taxon=taxon, paragraphs=paragraphs)

        all_traits = pages[taxon].all_traits
        missing.get_missing_traits(all_traits)
        nectaries_secretion.get_nectaries_secretion(all_traits)
        phyllotaxy.get_missing_phyllotaxy(all_traits)
        for trait in all_traits:
            if trait._paragraph not in pages[taxon].paragraphs:
                paragraph = Paragraph(
                    label=trait._paragraph,
                    text=f"**** '{trait._paragraph}' paragraph missing **** ",
                )
                pages[taxon].paragraphs[trait._paragraph] = paragraph
            pages[taxon].paragraphs[trait._paragraph].traits.append(trait)

    return pages


def get_paragraphs(soup):
    paragraphs: dict[str, Paragraph] = {}

    for para in soup.find_all("p"):
        text = " ".join(para.text.split())

        first_sent, *_ = text.split(".")
        first_sent = first_sent.lower()

        for label, pipeline in util.PIPELINES.items():
            if pipeline.pattern in first_sent:
                traits = util.get_traits(label, text)
                paragraphs[label] = Paragraph(label=label, text=text, traits=traits)
                for trait in traits:
                    trait._paragraph = label

    return paragraphs
