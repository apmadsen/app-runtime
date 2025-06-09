[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [runtime](/docs/0.0/runtime/module.md) >
   [locking](/docs/0.0/runtime/locking/module.md) >
    Handle

# Handle class : Finalizable

The Handle class represents a filesystem handle to a file used for locking purposes. It's intended for internal use only.

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