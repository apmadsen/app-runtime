[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [application](/docs/0.0/runtime/application/module.md) >
    prevent_pythonpath

## prevent_pythonpath(suppress_info: _bool_ = _True_) -> None

Prevents paths in development from entering the sys.path, either because the current working directory contains a python init script, or because one or more paths are injected via the PYTHONPATH environment variable.