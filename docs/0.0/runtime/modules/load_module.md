[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [modules](/docs/0.0/runtime/modules/module.md) >
    load_module

## load_module(module_path: _str_) -> _ModuleType_

Load module given its full path.

### Example:

```python
from runtime.modules import load_module

try:
    module = load_module("some_module.py")

    ...
except FileNotFoundError:
    ... # module not found
```

## load_module(module_path: _str_, module_name: _str_) -> _ModuleType_

Load module by name from root path.

### Example:

```python
from runtime.modules import load_module

try:
    module = load_module("path/to/modules", "some_module")

    ...
except FileNotFoundError:
    ... # module not found
```