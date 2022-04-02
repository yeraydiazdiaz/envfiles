.PHONY: install-dev
.SILENT: install-dev

install-dev:
	pip install -U pip
	pip install -e .[dev]
