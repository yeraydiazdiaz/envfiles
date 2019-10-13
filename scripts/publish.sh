#!/bin/sh -e

PACKAGE=src/envfiles

find ${PACKAGE} -type f -name "*.py[co]" -delete
find ${PACKAGE} -type d -name __pycache__ -delete

python setup.py sdist bdist_wheel
twine upload dist/*

echo "You probably want to also tag the version now..."
