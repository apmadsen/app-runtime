# pyright: basic
from os import path, remove
from sys import modules
from typing import cast
from pytest import raises as assert_raises, fixture

from runtime.core.application import SINGLE_INSTANCE_FILENAME
from runtime.core.locking import get_shared_lock_path, lock_file
from runtime.core.locking.handle import Handle

from runtime.locking import LockException
from runtime.application import (
    single_instance, is_interactive, is_python_shell,
    get_application_path, get_main_module, get_main_package,
    get_installalled_apps_path, get_auxilary_packages
)

def test_single_instance():
    file_path = get_shared_lock_path(SINGLE_INSTANCE_FILENAME)

    if path.isfile(file_path):
        remove(file_path)

    handle = cast(Handle, single_instance())
    assert path.isfile(handle.filename)
    handle.acquire()
    handle.release()
    assert not path.isfile(handle.filename)

    # handle1 = cast(Handle, single_instance())
    # handle2 = cast(Handle, lock_file(handle1.filename))

    # handle2.acquire()
    # self.assertRaises(LockException, handle1.acquire)
    # x=0

    # handle1.finalize()


def test_is_interactive():
    result = is_interactive()
    assert not result

def test_is_python_shell():
    result = is_python_shell()
    assert not result

def test_get_application_path():
    result = get_application_path()
    assert result == getattr(modules["__main__"], "__file__")

def test_get_installed_apps_path():
    result = get_installalled_apps_path(False)
    assert path.isdir(result)
    result = get_installalled_apps_path(True)
    assert path.isdir(result)

def test_get_main_module():
    result = get_main_module()
    assert result == modules["__main__"]

def test_get_main_package():
    result = get_main_package()
    from importlib.metadata import version
    assert result.name == getattr(modules["__main__"], "__package__")
    assert result.version == version(getattr(modules["__main__"], "__package__"))

def test_get_auxilary_packages():
    mp = get_main_package()
    result = get_auxilary_packages()
    assert mp.name not in result

