from pathlib import Path

from bs4 import BeautifulSoup


def read(input_dir: Path, pattern: str) -> dict[str, str]:
    paragraphs: dict[str, str] = {}

    paths = sorted(input_dir.glob("*.htm*"))

    for path in paths:
        with path.open("rb") as in_file:
            raw = in_file.read()

        soup = BeautifulSoup(raw, features="lxml")

        taxon = soup.title.text

        paragraphs[taxon] = get_paragraph(soup, pattern)

    return paragraphs


def get_paragraph(soup, pattern):
    for para in soup.find_all("p"):
        text = " ".join(para.text.split())

        first, *_ = text.split(".")
        first = first.lower()

        if pattern in first:
            return text

    return ""
