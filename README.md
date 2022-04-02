# envfiles: Simple layered loading of env files

So you've set up your app to configure itself from environment variables,
awesome, well done!

Now all you need to do is to make sure *all of them* are present before
running your app. Good thing we have env files, right? But wait, they can't
be the same all the time, they're slightly different for tests, Docker,
and for local development... that's annoying.

No biggie though, we can just create several env files and load them...
But that would fail in prod because the env files won't be there...
We could load them only if they exist but that's kinda hacky...

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

Note the first line `# >> base.env`, the `# >> ` is an arbitrary prefix, the
`base.env` is a path *relative to the file being read*.

Then point envfiles to the file you want to load and let it resolve the variables.
For example, you could define *one* environment variable, `ENV_FILE` for instance,
containing a relative path to the env file you want to load:

```python
import envfiles

env_vars = envfiles.load_env_files(os.getenv("ENV_FILE"))
assert env_vars == {
    "CACHE_ENABLED": "0",
    "DATABASE_HOST": "localhost",
    "DATABASE_NAME": "myapp_test",
}
```

Note `envfiles` will **not** mess with your `os.environ`, or attempt parsing or
(de)serializing variables. The output is a dictionary of strings to strings,
what you do with it is entirely your business. Typically you would combine it
with `os.environ` and pass it to your app's configuration solution.

For example, if you're using
[`environ-config`](https://github.com/hynek/environ-config) 💚

```python
import environ
import envfiles
from settings import MyConfig  # your environ-config Config class

env_vars = envfiles.load(os.getenv("ENV_FILE"))

env_vars.update(os.environ)  # actual environment variables have preference
config = environ.to_config(MyConfig, environ=env_vars)
```

## Why?

Frustration, mostly. I've had this issue more times than I can count. I've tried
different libraries but none of them supported layering or sort of did but
messed with the `os.environ` in surprising ways.

The idea behind `envfiles` is to declaratively define how the env files are loaded
and let you use whatever configuration solution you want.

Configuration is the first thing your app does, it should be as quick and
straightforward as possible.

## Alternatives

If `envfiles` is not what you were looking for here are some other options you
may want to consider, all of them more mature and featured than `envfiles`:

- [`dotenv`](https://github.com/theskumar/python-dotenv)
- [`environs`](https://github.com/sloria/environs)
