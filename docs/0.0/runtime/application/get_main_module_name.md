[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [application](/docs/0.0/runtime/application/module.md) >
    get_main_module

## get_main_module_name() -> _ModuleType_

Returns the real name of the main module. In normal circumstances the `module.__package__` attribute is used, but if that's not available, the filename of the module is used instead.

In some occations, the result may be "__main__".