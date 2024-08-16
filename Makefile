.PHONY: test install dev clean
.ONESHELL:

# Many requests to simplify this script, so here we are.

test:
	. .venv/bin/activate
	export MOCK_TRAITER=1
	python3.11 -m unittest discover
	export MOCK_TRAITER=0

install:
	test -d .venv || python3.11 -m venv .venv
	. .venv/bin/activate
	./.venv/bin/python3.11 -m pip install -U pip setuptools wheel
	./.venv/bin/python3.11 -m pip install git+https://github.com/rafelafrance/common_utils.git@main#egg=common_utils
	./.venv/bin/python3.11 -m pip install git+https://github.com/rafelafrance/spell-well.git@main#egg=spell-well
	./.venv/bin/python3.11 -m pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
	./.venv/bin/python3.11 -m pip install git+https://github.com/rafelafrance/FloraTraiter.git@main#egg=FloraTraiter
	./.venv/bin/python3.11 -m pip install .
	./.venv/bin/python3.11 -m spacy download en_core_web_md

dev:
	test -d .venv || python3.11 -m venv .venv
	. .venv/bin/activate
	./.venv/bin/python3.11 -m pip install -U pip setuptools wheel
	./.venv/bin/python3.11 -m pip install -e ../../misc/common_utils
	./.venv/bin/python3.11 -m pip install -e ../../misc/spell-well
	./.venv/bin/python3.11 -m pip install -e ../../traiter/traiter
	./.venv/bin/python3.11 -m pip install -e ../../traiter/FloraTraiter
	./.venv/bin/python3.11 -m pip install -e .[dev]
	./.venv/bin/python3.11 -m spacy download en_core_web_md
	pre-commit install

clean:
	rm -r .venv
	find -iname "*.pyc" -delete
