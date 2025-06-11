[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [application](/docs/0.0/runtime/application/module.md) >
    single_instance

## single_instance() -> _ContextManager[Any]_

Returns a SingleInstance context, which ensures that application is only running in one instance.

Internally a locking.Handle is created and returned.

### Example:

```python
from runtime.application import single_instance, SingleInstanceException

try:
    with single_instance():
        ...

except SingleInstanceException:
    print("Another instance of this application is already running!")
```