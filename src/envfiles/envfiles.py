import typing

from pathlib import Path


class EnvFilesError(Exception):
    pass


NESTED_ENV_FILE_PREFIX = "# >> "


def load(
    env_file_path: typing.Union[str, Path], nested_prefix: str = NESTED_ENV_FILE_PREFIX
) -> typing.Dict[str, str]:
    """Loads env files from a relative path to the current working directory.

    Env files contain the familiar KEY=VALUE lines, with VALUE optionally
    being quoted, the return dict will strip the quotes and remove any
    trailing whitespace. Note all names and values are returned as strings.

    Env files may also contain comments in the form of
    `# >> PATH_TO_ENV_FILE`, this will signal EnvFiles to load the nested
    path before continuing.

    Nested env paths need not be defined at the top of the file but
    their contents *will override* any previous entries in the containing
    file.
    """
    path = Path.cwd() / Path(env_file_path)
    if not path.exists():
        raise EnvFilesError(f"Path {path} does not exist")

    env_vars = {}
    with open(path, "r") as fd:
        for line in fd.readlines():
            line = line.strip()
            if line.startswith(nested_prefix):
                nested_env_path = line[len(nested_prefix) :]
                if nested_env_path == env_file_path:
                    raise EnvFilesError(
                        f"Self referencing nested path {nested_env_path}"
                    )
                relative_nested_path = path.parent / nested_env_path
                env_vars.update(load(relative_nested_path))
            elif line.startswith("#") or not line:
                continue
            else:
                name, value = process_env_line(line)
                env_vars[name] = value

    return env_vars


def process_env_line(line: str) -> typing.Tuple[str, str]:
    """Returns a 2-tuple of (name, value) for a line in an env file."""
    try:
        name, value = line.strip().split("=", maxsplit=1)
    except ValueError as exc:
        raise EnvFilesError(f"Error processing line {line}") from exc

    return name, process_value(value)


def process_value(value: str) -> str:
    """Returns a processed value for an environment variable."""
    if len(value) > 0 and value[0] == value[-1] == '"':
        return value[1:-1]

    return value
