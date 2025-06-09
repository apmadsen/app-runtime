[![Test](https://github.com/apmadsen/app-runtime/actions/workflows/python-test.yml/badge.svg)](https://github.com/apmadsen/app-runtime/actions/workflows/python-test.yml)
[![Coverage](https://github.com/apmadsen/app-runtime/actions/workflows/python-test-coverage.yml/badge.svg)](https://github.com/apmadsen/app-runtime/actions/workflows/python-test-coverage.yml)
[![Stable Version](https://img.shields.io/pypi/v/app-runtime?label=stable&sort=semver&color=blue)](https://github.com/apmadsen/app-runtime/releases)
![Pre-release Version](https://img.shields.io/github/v/release/apmadsen/app-runtime?label=pre-release&include_prereleases&sort=semver&color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/app-runtime)
[![PyPI Downloads](https://static.pepy.tech/badge/app-runtime/week)](https://pepy.tech/projects/app-runtime)

# app-runtime
> Provides tools for handling the context of a Python application, including getting system, user and application info.

## Example

```python
from runtime.application import (
    single_instance, is_interactive, get_main_package,
    hook_terminate, TerminateException
)
from runtime.user import get_username, is_elevated

hook_terminate()
username = get_username()
pkg = get_main_package()
interactive = is_interactive()

def output(line: str):
    if interactive:
        print(line)

with single_instance():
    try:
        output(f"Hello {'admin ' if is_elevated() else ''}{username}, this is {pkg.name} ver. {pkg.version}")
    except TerminateException:
        output(f"Bye {username}")
    except:
        output("An unexpected error ocurred")

```



## Full documentation

[Go to documentation](https://github.com/apmadsen/app-runtime/blob/main/docs/documentation.md)