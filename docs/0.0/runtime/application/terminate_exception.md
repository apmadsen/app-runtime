[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [application](/docs/0.0/runtime/application/module.md) >
    TerminateException

# TerminateException : Exception

The `TerminateException` exception is raised when application receives a terminate or interrupt signal.

The hook_terminate() functions is required to set everything up.

### Example:

```python
from runtime.application import hook_terminate, TerminateException

try:
    hook_terminate()

    ...
except TerminateException:
    ... # cleanup tasks
```