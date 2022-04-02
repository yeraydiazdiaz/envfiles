import nox


nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True

source_files = ("src/envfiles", "tests", "noxfile.py")


@nox.session
def lint(session):
    session.install("-e", ".[dev]")
    session.run("autoflake", "--in-place", "--recursive", *source_files)
    session.run("seed-isort-config", "--application-directories=src/envfiles")
    session.run("isort", "--project=envfiles", *source_files)
    session.run("black", "--target-version=py36", *source_files)


@nox.session
def check(session):
    session.install("-e", ".[dev]")
    session.run("black", "--check", "--diff", "--target-version=py36", *source_files)
    session.run("flake8", *source_files)
    session.run("mypy", "src/envfiles")
    session.run(
        "isort", "--check", "--diff", "--project=envfiles", "--recursive", *source_files
    )


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10"])
def test(session):
    session.install("-e", ".[test]")
    session.run("python", "-m", "pytest", *session.posargs)


@nox.session
def publish_test(session):
    _publish(session, "testpypi")


@nox.session
def publish(session):
    _publish(session, None)


def _publish(session, repository):
    session.install("flit")
    url = "pypi.org"
    if repository == "testpypi":
        url = f"test.{url}"

    confirm = input(f"Are you sure you want to release to {url}? ")
    if confirm.lower().strip() not in ("y", "yes"):
        session.error("Aborting as requested")

    args = ["flit", "publish"]
    if repository is not None:
        args += ["--repository", repository]

    session.run(*args)
