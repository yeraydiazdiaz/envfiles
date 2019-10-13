# `envfiles`: Simple layered loading of env files for your [12-factor](https://12factor.net/) app

You've set up your app to configure itself from environment variables,
awesome, well done. Now all you need to do is to export *all of them* before
running your app. Oh, and also they need to be slightly different in Docker,
and tests, and for local development...

Wouldn't it be neat if we could layer env files? Imagine a `base.env`:

```
CACHE_ENABLED=1
DATABASE_HOST=localhost
DATABASE_NAME=myapp
```

A `test.env` that overrides it:

```
# >> base.env
CACHE_ENABLED=0
DATABASE_NAME=myapp_test
```

And then define *one* environment variable, `ENV_FILE` in this example, with a
relative path to the env file you want to load:

```python
import envfiles

env_vars = envfiles.load_env_files(os.getenv("ENV_FILE"))
assert env_vars == {
    "CACHE_ENABLED": "1",
    "DATABASE_HOST": "localhost",
    "DATABASE_NAME": "myapp_test",
}
```

Note `envfiles` will *not* mess with your `os.environ`, or attempt parsing or
(de)serializing variables. The output is a dictionary of strings to strings,
what you do with it is entirely your business.

You can simply update `os.environ` with
the result of `envfiles` and let your configuration library/code pick it up.
Do note that if you do this the actual environment variables will be overridden
by the result of `envfiles`.

Instead, I suggest updating the results with `os.environ` and passing it to
[`environ-config`](https://github.com/hynek/environ-config) 💚

```python
import environ
import envfiles
from settings import MyConfig  # your environ-config Config class

env_vars = envfiles.load_env_files(os.getenv("ENV_FILE"))

env_vars.update(os.environ)
config = environ.to_config(MyConfig, environ=env_vars)
```

## Why?

Frustration, mostly. I've had this issue more times than I can count. I've tried
different libraries but none of them supported layering or they messed with the
`os.environ` in surprising ways.

The idea behind `envfiles` is to solve reading layered env files and let you
use whatever configuration solution you want. Configuration is the first
thing your app does, it should be as quick and straightforward as possible.

## Alternatives

If `envfiles` is not what you were looking for here are some other options you
may want to consider, all of them more mature and featured than `envfiles`:

- [`dotenv`](https://github.com/theskumar/python-dotenv)
- [`environs`](https://github.com/sloria/environs)
