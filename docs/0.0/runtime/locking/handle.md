[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [locking](/docs/0.0/runtime/locking/module.md) >
    Handle

# Handle class : Finalizable

The Handle class represents a filesystem handle to a file used for locking purposes. It's intended for internal use only and the suggested implementation is `lock_handle()`.

## Properties

### name -> _str | None_

The name of the handle if any.

### filename -> _str_

The filename of the handle.

## Functions

### acquire() -> _None_

Acquires the lock.

### release() -> _None_

Releases the lock.


## Example:

```python
from io import IOBase
from os import remove
from runtime.locking import Handle, LockException

def fn_continuation(acquired: bool, handle: Handle, fp: IOBase):
    remove(handle.filename)

try:
    filename = "tests/lockfile.lock"
    file = open(filename, "w")
    with Handle(file, filename, "Lock", continuation = fn_continuation):
        ...

except LockException:
    ... # a handle exists and is already locked
```