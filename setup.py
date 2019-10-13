import codecs
import os
import re

from copy import deepcopy

from setuptools import find_packages, setup


HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


def load_requirements_file(requirement_filename):
    path = os.path.join(HERE, "requirements", requirement_filename)
    lines = read(path).strip().split("\n")
    return [
        line
        for line in lines
        if line and not line.startswith("#") and not line.startswith("-r")
    ]


NAME = "envfiles"
META_PATH = os.path.join("src", "envfiles", "__init__.py")
META_FILE = read(META_PATH)
PACKAGES = find_packages(where="src")
KEYWORDS = ["environment", "variables", "12-factor"]
PROJECT_URLS: dict = {}
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = load_requirements_file("base.txt")
EXTRAS_REQUIRE = {"tests": load_requirements_file("test.txt")}
EXTRAS_REQUIRE["dev"] = deepcopy(EXTRAS_REQUIRE["tests"])
EXTRAS_REQUIRE["dev"].extend(load_requirements_file("dev.txt"))
VERSION = find_meta("version")
URL = find_meta("url")
LONG = read("README.md")


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=URL,
        project_urls=PROJECT_URLS,
        version=VERSION,
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=LONG,
        long_description_content_type="text/markdown",
        packages=PACKAGES,
        package_dir={"": "src"},
        python_requires=">=3.7.*",
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        include_package_data=True,
    )
