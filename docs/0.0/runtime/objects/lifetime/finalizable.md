[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [objects](/docs/0.0/runtime/objects/module.md) >
    [lifetime](/docs/0.0/runtime/objects/lifetime/module.md) >
     Finalizable

# Finalizable : abc.ABC

Base class for implementation of the Finalizable pattern. When instances of a derived class are garbage collected, finalization takes place automatically.

## Properties

### finalized -> _bool_

Indicates if object has been finalized or not.

### finalizing -> _bool_

Indicates if object is in the process of finalizing or not.

## Functions

### finalize() -> _None_

Initiates the finalization process manually.

## Abstract functions

### __finalize__() -> _None_

This function is invoked when finalization process is initiated.


## Example:

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