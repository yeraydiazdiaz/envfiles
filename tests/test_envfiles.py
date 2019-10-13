from io import StringIO

import pytest

import envfiles


def test_path_does_not_exist():
    with pytest.raises(envfiles.EnvFilesError):
        envfiles.load("path/to/nowhere")


@pytest.mark.parametrize(
    "contents,expected",
    [
        ("FOO=bar", {"FOO": "bar"}),
        ("EMPTY=", {"EMPTY": ""}),
        ('FOO=bar\nBAR="baz"', {"FOO": "bar", "BAR": "baz"}),
        ('FOO=bar\n# comment\nBAR="baz"\n\n', {"FOO": "bar", "BAR": "baz"}),
    ],
)
def test_env_file(mocker, contents, expected):
    mocker.patch("envfiles.envfiles.open", return_value=StringIO(contents))
    mocker.patch("envfiles.envfiles.Path.exists", return_value=True)

    env_vars = envfiles.load("some/path")

    assert env_vars == expected


def test_nested_env_file(mocker):
    contents = "# >> base.env\nBAR=baz"
    base_contents = "FOO=bar"
    mocker.patch(
        "envfiles.envfiles.open",
        side_effect=[StringIO(contents), StringIO(base_contents)],
    )
    mocker.patch("envfiles.envfiles.Path.exists", return_value=True)

    env_vars = envfiles.load("some/path")

    assert env_vars == {"FOO": "bar", "BAR": "baz"}


def test_nested_env_file_overrides_previous_values(mocker):
    contents = "FOO=override-me\n# >> base.env\nBAR=baz"
    base_contents = "FOO=bar"
    mocker.patch(
        "envfiles.envfiles.open",
        side_effect=[StringIO(contents), StringIO(base_contents)],
    )
    mocker.patch("envfiles.envfiles.Path.exists", return_value=True)

    env_vars = envfiles.load("some/path")

    assert env_vars == {"FOO": "bar", "BAR": "baz"}


def test_nested_env_file_fails_if_self_referencial(mocker):
    contents = "# >> local.env\nBAR=baz"
    mocker.patch("envfiles.envfiles.open", return_value=StringIO(contents))
    mocker.patch("envfiles.envfiles.Path.exists", return_value=True)

    with pytest.raises(envfiles.EnvFilesError):
        envfiles.load("local.env")


def test_malformed_line(mocker):
    with pytest.raises(envfiles.EnvFilesError):
        envfiles.envfiles.process_env_line("FOO")


@pytest.mark.integration
def test_layered_env_files():
    env_vars = envfiles.load("tests/assets/test.env")

    assert env_vars == {
        "CACHE_ENABLED": "0",
        "DATABASE_HOST": "localhost",
        "DATABASE_NAME": "myapp_test",
    }
