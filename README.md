# AngiospermTraiter ![Python application](https://github.com/rafelafrance/AngiospermTraiter/workflows/CI/badge.svg)

Extract traits about plants from treatments.

I should also mention that this repository builds upon other repositories:

- `traiter`: This is the base code for all the rule-based parsers (aka traiters) that I write. The details change but the underlying process is the same for all.
  - `https://github.com/rafelafrance/traiter`

## All righty, what's this then?

**Challenge**: Extract trait information from plant treatments. That is, if I'm given treatment text like: (Reformatted to emphasize targeted traits.)

**TODO**

## Rule-based parsing strategy

1. There is a lot of overlap in trait terms, for example `biseriate` is used for `perianth`, `androecium`, etc. Fortunately, each major plant section has its own paragraph, so I can split the text into paragraphs and parse each separately and with its own vocabulary and patterns.
2. I label terms using Spacy's phrase and rule-based matchers.
3. Then I match terms using rule-based matchers to yield a trait.

For example, given the text: `Gynoecium 1–3–5(–6) carpelled.`:

- NOTE: Each web page refers to a specific taxonomic unit, in this case a family, so I know that from other information on the page, like the title.

1. First I recognize that this is a text paragraph dealing with gynoecia, so I use a parser tailored with those terms.
   1. The first sentence in the paragraph contains the word `Gynoecium`.
2. I then recognize other various terms in the paragraph.
   1. `1–3–5(–6)` is a numeric range term. These are integers and there are no units (like cm) making it a count range and not a measurement range like length or width.
      - `1` = the minimum value seen
      - `3` = the commonly seen low value
      - `5` = the commonly seen high value
      - `6` = the maximum value seen
   2. `carpelled` is term applied to gynoecia.
3. The parser recognizes the `<range> <carpelled>` pattern, and gets a carpel count for this plant taxon.

There are, of course, complications and subtleties not outlined above, but you should get the gist of what is going on here.

## Install

You will need to have Python3.11+ installed, as well as pip, a package manager for Python.
You can install the requirements into your python environment like so:

```bash
git clone https://github.com/rafelafrance/AngiospermTraiter.git
cd AngiospermTraiter
make install
```

Every time you run any script in this repository, you'll have to activate the virtual environment once at the start of your session.

```bash
cd AngiospermTraiter
source .venv/bin/activate
```

### Extract traits

You'll need some treatment text files. One treatment per file.

Example:

```bash
parse-treatments --treatment-dir /path/to/treatments --json-dir /path/to/output/traits --html-file /path/to/traits.html
```

## Tests

There are tests which you can run like so:

```bash
make test
```

## Raw data

The target data is generously provided in this [zip file](https://www.delta-intkey.com/angio/angiodata.zip) by DELTA IntKey.
