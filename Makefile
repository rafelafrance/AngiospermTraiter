.PHONY: test install dev clean
.ONESHELL:

# Many requests to simplify this script, so here we are.

test:
	. .venv/bin/activate
	export MOCK_TRAITER=1
	python -m unittest discover
	export MOCK_TRAITER=0

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
