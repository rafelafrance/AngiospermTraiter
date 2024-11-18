.PHONY: test install dev clean parse
.ONESHELL:

TODAY = $(shell date -I)
INPUT_DIR ?= ./data/angiodata/www
HTML_FILE ?= ./data/output/parse_families_$(TODAY).html
CSV_FILE ?= ./data/output/parse_families_$(TODAY).csv

test:
	. .venv/bin/activate
	python -m unittest discover

install:
	test -d .venv || python3.12 -m venv .venv
	. .venv/bin/activate
	./.venv/bin/python -m pip install -U pip setuptools wheel
	./.venv/bin/python -m pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
	./.venv/bin/python -m pip install .
	./.venv/bin/python -m spacy download en_core_web_md

dev:
	test -d .venv || python3.12 -m venv .venv
	. .venv/bin/activate
	./.venv/bin/python -m pip install -U pip setuptools wheel
	./.venv/bin/python -m pip install -e ../../traiter/traiter
	./.venv/bin/python -m pip install -e .[dev]
	./.venv/bin/python -m spacy download en_core_web_md
	pre-commit install

clean:
	rm -r .venv
	find -iname "*.pyc" -delete

parse:
	angiosperm/parse_families.py \
		--input-dir $(INPUT_DIR) \
		--html-file $(HTML_FILE) \
		--csv-file $(CSV_FILE)
