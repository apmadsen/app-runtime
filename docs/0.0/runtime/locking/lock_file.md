[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [locking](/docs/0.0/runtime/locking/module.md) >
    lock_file

## lock_file(file_path: _str_) -> _ContextManager[Any]_

Returns a Handle object for specified file_path.

### Example:

```python
from runtime.locking import lock_file, LockException

try:
    with lock_file("./lockfile.lock"):
        ...
except LockException:
    ... # file exists and is already locked
```