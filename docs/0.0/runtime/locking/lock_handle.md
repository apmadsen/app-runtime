[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [locking](/docs/0.0/runtime/locking/module.md) >
    lock_handle

## lock_handle(name: _str_) -> _ContextManager[Any]_

Returns a named Handle object in the common system path for shared locks.

### Example:

```python
from runtime.locking import lock_handle, LockException

try:
    with lock_handle("lock"):
        ...
except LockException:
    ... # a handle exists and is already locked
```