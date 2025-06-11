[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [application](/docs/0.0/runtime/application/module.md) >
    get_installalled_apps_path

## get_installalled_apps_path(*, ensure_exists: _bool_ = _False_, elevated: _bool_ = _USER_ELEVATED_) -> _str_

Gets the default path for installed user applications.

The `ensure_exists` argument specifies whether or not creation of nonexistent folder should be attempted. Applies to elevated user context only.

The `elevated` argument has a determining factor on the location, being under the local users home folder or in a system folder.