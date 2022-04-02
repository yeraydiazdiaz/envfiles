import nox


nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True

source_files = ("src/envfiles", "tests", "setup.py", "noxfile.py")


@nox.session
def lint(session):
    session.install(
        "--upgrade", "autoflake", "black", "flake8", "isort", "seed-isort-config"
    )

    session.run("autoflake", "--in-place", "--recursive", *source_files)
    session.run("seed-isort-config", "--application-directories=src/envfiles")
    session.run("isort", "--project=envfiles", "--recursive", "--apply", *source_files)
    session.run("black", "--target-version=py36", *source_files)


@nox.session
def check(session):
    session.install(
        "--upgrade",
        "black",
        "flake8",
        "flake8-bugbear",
        "flake8-comprehensions",
        "flake8-pie",
        "isort",
        "mypy",
    )

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
