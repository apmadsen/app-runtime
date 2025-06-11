[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [objects](/docs/0.0/runtime/objects/module.md) >
    [lifetime](/docs/0.0/runtime/objects/lifetime/module.md) >
     FinalizedError

# FinalizedError class : BaseException

The FinalizedError exception is raised when trying to finalize an already finalized object.

### Example:

```python
from runtime.objects.lifetime import Finalizable, FinalizedError

try:
    class Test(Finalizable):
        _is_finalized = False

        def __finalize__(self) -> None:
            self._is_finalized = True

    instance = Test()

    ...

    instance.finalize()

except FinalizedError:
    ... # instance has been finalized
```