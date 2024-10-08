# AngiospermTraiter ![Python application](https://github.com/rafelafrance/AngiospermTraiter/workflows/CI/badge.svg)

Extract traits about plants from treatments.

I should also mention that this repository builds upon other repositories:
- `traiter`: This is the base code for all the rule-based parsers (aka traiters) that I write. The details change but the underlying process is the same for all.
  - `https://github.com/rafelafrance/traiter`

## All righty, what's this then?

**Challenge**: Extract trait information from plant treatments. That is, if I'm given treatment text like: (Reformatted to emphasize targeted traits.)

**TODO**

## Rule-based parsing strategy
1. There is a lot of overlap in trait terms, for example biseriate is used for perianth, androecium, etc. Fortunately, each major plant section has its own paragraph, so I can split the text into paragraphs and parse each separately and with its own vocabulary and patterns.
2. I label terms using Spacy's phrase and rule-based matchers.
3. Then I match terms using rule-based matchers to yield a trait.

For example, given the text: `Petiole 1-2 cm.`:
- I recognize vocabulary terms like:
    - `Petiole` is plant part
    - `1` a number
    - `-` a dash
    - `2` a number
    - `cm` is a unit notation
- Then I group tokens. For instance:
    - `1-2 cm` is a range with units which becomes a size trait.
- Finally, I associate the size with the plant part `Petiole` by using another pattern matching parser.

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
