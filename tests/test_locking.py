# pyright: basic
from os import path, remove
from typing import cast
from io import IOBase
from sys import platform

from milieu.internal.app.locking import get_shared_lock_path
from milieu.internal.app.locking.handle import Handle
from milieu.internal.app.locking.log import log
from milieu.locking import LockException, lock_handle, lock_file
from milieu.objects.lifetime import FinalizedError

from tests.testbase import TestBase

class TestLocking(TestBase):
    def test_handle(self):
        log.addHandler(self.test_log_handler)
        filename = path.join(self._base_dir, f"{self.id()}.lock")
        file = open(filename, "w")
        file.write("test")
        pos = file.tell()
        continuation_hit = []

        def fn_continuation(acquired: bool, handle: IOBase, filename: str):
            continuation_hit.append(int(acquired))

        try:
            handle1 = Handle(file, filename, self.id(), continuation = fn_continuation)
            handle2 = Handle(file, filename, continuation = fn_continuation)

            self.assertEqual(handle1.name, self.id())

            with handle1:
                self.assertEqual(file.tell(), pos)
                self.assertRaises(LockException, handle2.acquire)

            self.assertIn(1, continuation_hit)
            self.assertIn(0, continuation_hit)
            self.assertRaises(FinalizedError, handle1.acquire)
            self.assertRaises(FinalizedError, handle1.release)

            self.assertTrue(handle1.finalized)
            self.assertFalse(handle2.finalized)
            self.assertTrue(file.closed)

        finally:
            file.close()


    def test_lock_file(self):
        log.addHandler(self.test_log_handler)
        filename = path.join(self._base_dir, f"{self.id()}.lock")
        file = open(filename, "w")

        try:
            handle1 = lock_file(filename)
            handle2 = Handle(file, filename)

            with handle1:
                self.assertRaises(LockException, handle2.acquire)

            self.assertFalse(file.closed) # lock_file doesn't close file
        finally:
            file.close()

    def test_lock_handle(self):
        log.addHandler(self.test_log_handler)
        name = self.id()
        file_path = get_shared_lock_path(name)

        if path.isfile(file_path):
            remove(file_path)

        handle = cast(Handle, lock_handle(name))
        self.assertEqual(path.abspath(handle.filename), path.abspath(file_path))

        try:
            self.assertRaises(FileExistsError, lock_handle, name)
        finally:
            handle.finalize()

        self.assertTrue(handle.finalized)

    def tearDown(self):
        pass
