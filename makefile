.PHONY: pin-requirements install-dev package release-test release-pypi
.SILENT: pin-requirements install-dev package release-test release-pypi

pin-requirements:
	pip-compile requirements/base.in --output-file requirements/base.txt

install-dev:
	pip install -e .[dev]

package:
	rm -fr dist/*
	python setup.py sdist
	python setup.py bdist_wheel --universal

release-test: package
	@echo "Are you sure you want to release to test.pypi.org? [y/N]" && \
		read ans && \
		[ $${ans:-N} = y ] && \
		twine upload --repository testpypi dist/*

release-pypi: package
	@echo "Are you sure you want to release to pypi.org? [y/N]" && \
		read ans && \
		[ $${ans:-N} = y ] && \
		twine upload dist/*
