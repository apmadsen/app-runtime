[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [application](/docs/0.0/runtime/application/module.md) >
    SingleInstanceException

# SingleInstanceException class : Exception

The `SingleInstanceException` exception is raised when another instance of the application is already running in the same user context.

The single_instance() function is required to set everything up.

### Example:

```python
from runtime.application import single_instance, SingleInstanceException

try:
    with single_instance():
        ...

except SingleInstanceException:
    print("Another instance of this application is already running!")
```