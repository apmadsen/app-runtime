# pyright: basic
from os import path, remove
from sys import modules
from typing import cast

from tests.testbase import TestBase

from milieu.internal.app.application import SINGLE_INSTANCE_FILENAME
from milieu.internal.app.locking import log, get_shared_lock_path, lock_file
from milieu.internal.app.locking.handle import Handle
from milieu.locking import LockException
from milieu.application import (
    single_instance, is_interactive, is_python_shell,
    get_application_path, get_main_module, get_main_package,
    get_installalled_apps_path, get_auxilary_packages
)

class TestApplication(TestBase):

    def test_single_instance(self):
        log.addHandler(self.test_log_handler)
        file_path = get_shared_lock_path(SINGLE_INSTANCE_FILENAME)

        if path.isfile(file_path):
            remove(file_path)

        handle = cast(Handle, single_instance())
        self.assertTrue(path.isfile(handle.filename))
        handle.acquire()
        handle.release()
        self.assertFalse(path.isfile(handle.filename))

        # handle1 = cast(Handle, single_instance())
        # handle2 = cast(Handle, lock_file(handle1.filename))

        # handle2.acquire()
        # self.assertRaises(LockException, handle1.acquire)
        # x=0

        # handle1.finalize()


    def test_is_interactive(self):
        result = is_interactive()
        self.assertFalse(result)

    def test_is_python_shell(self):
        result = is_python_shell()
        self.assertFalse(result)

    def test_get_application_path(self):
        result = get_application_path()
        self.assertEqual(result, getattr(modules["__main__"], "__file__"))

    def test_get_main_module(self):
        result = get_main_module()
        self.assertEqual(result, modules["__main__"])

    def test_get_main_package(self):
        result = get_main_package()
        from importlib.metadata import version
        self.assertEqual(result.name, getattr(modules["__main__"], "__package__"))
        self.assertEqual(result.version, version(getattr(modules["__main__"], "__package__")))

    def test_get_auxilary_packages(self):
        mp = get_main_package()
        result = get_auxilary_packages()
        self.assertNotIn(mp.name, result)


    def tearDown(self):
        pass
