.PHONY: pin-requirements install-dev
.SILENT: pin-requirements install-dev

pin-requirements:
	pip-compile requirements/base.in --output-file requirements/base.txt

install-dev:
	pip install -e .[dev]
