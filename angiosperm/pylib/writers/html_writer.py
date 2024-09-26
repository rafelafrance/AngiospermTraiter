import dataclasses
import html
import itertools
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import jinja2

from angiosperm.pylib.readers.family_html import Page

COLOR_COUNT = 15
BACKGROUNDS = itertools.cycle([f"cc{i}" for i in range(COLOR_COUNT)])

TEMPLATE_DIR: Path = Path.cwd() / "angiosperm/pylib/writers/templates"
TEMPLATE: str = "html_writer.html"


@dataclasses.dataclass
class HtmlParagraph:
    text: str
    traits: list[str]


@dataclasses.dataclass
class HtmlPage:
    taxon: str
    paragraphs: list[HtmlParagraph] = dataclasses.field(default_factory=list)


class CssClasses:
    def __init__(self):
        self.classes = {}

    def __getitem__(self, key):
        if key not in self.classes:
            self.classes[key] = next(BACKGROUNDS)
        return self.classes[key]


def write(input_pages: dict[str, Page], html_file: Path):
    css_classes = CssClasses()
    html_pages = []

    for input_page in input_pages.values():
        paras = []
        for para in input_page.paragraphs:
            formatted = format_paragraph(para.text, para.traits, css_classes)
            traits = format_traits(para.text, para.traits, css_classes)
            paras.append(HtmlParagraph(formatted, traits))
        html_pages.append(Page(taxon=input_page.taxon, paragraphs=paras))

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True
    )

    template = env.get_template(TEMPLATE).render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        file_name=html_file.stem,
        pages=html_pages,
    )

    with html_file.open("w") as html:
        html.write(template)


def format_paragraph(
    raw_text: str, traits: list[dict[str, any]], css_classes: CssClasses
) -> str:
    """Wrap traits in the text with <spans> that can be formatted with CSS."""
    frags = defaultdict(lambda: {"raw": "", "cls": "", "title": []})
    prev = 0

    for trait in traits:
        start = trait.start
        end = trait.end

        if prev < start:
            frags[prev, start]["raw"] = raw_text[prev:start]

        frags[start, end]["raw"] = raw_text[start:end]
        frags[start, end]["cls"] = css_classes[trait._trait]

        fields = [f"{k}: {v}" for k, v in trait.formatted().items()]
        title = "; ".join(fields)
        frags[start, end]["title"].append(title)

        prev = end

    if len(raw_text) > prev:
        frags[prev, len(raw_text)]["raw"] = raw_text[prev:]

    text = []
    for frag in frags.values():
        if frag["cls"]:
            title = "; ".join(frag["title"])
            cls = frag["cls"]
            text.extend(
                (
                    f'<span class="{cls}" title="{title}">',
                    html.escape(frag["raw"]),
                    "</span>",
                )
            )
        else:
            text.append(html.escape(frag["raw"]))

    text = "".join(text)
    return text


def format_traits(
    raw_text: str, traits: list[dict[str, any]], css_classes: CssClasses
) -> list[tuple[str, str]]:
    formatted = []
    merged = defaultdict(list)

    for trait in traits:
        for key, value in trait.formatted().items():
            cls = css_classes[trait._trait]
            title = "text: " + raw_text[trait.start : trait.end]
            field = f'<span class="value {cls}" title="{title}">{value}</span>'
            merged[key].append(field)

    for label, values in merged.items():
        label = f"<label>{label}:</label>"
        values = ", ".join(values)
        values = f'<span class="values">{values}</span>'
        formatted.append((label, values))

    return sorted(formatted)
