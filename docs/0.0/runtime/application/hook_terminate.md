[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [application](/docs/0.0/runtime/application/module.md) >
    hook_terminate

## hook_terminate() -> _None_

Hooks up interrupt and terminate handlers, which throws a `TerminateException` when signaled.

### Example:

```python
from runtime.application import hook_terminate, TerminateException

try:
    hook_terminate()

    ...
except TerminateException:
    ... # cleanup tasks
```