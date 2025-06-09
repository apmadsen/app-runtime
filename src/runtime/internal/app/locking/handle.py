from sys import platform
from io import IOBase
from typing import Any, Callable
from importlib import import_module

from milieu.internal.app.locking.lock_exception import LockException
from milieu.internal.app.objects.lifetime.finalized_error import FinalizedError
from milieu.internal.app.compat import fcntl, msvcrt
from milieu.internal.app.objects.lifetime.finalizable import Finalizable
from milieu.internal.app.locking.log import log

if platform == "win32":
    msvcrt = import_module("msvcrt")
else:
    fcntl = import_module("fcntl")


class Handle(Finalizable):
    __slots__ = [ "__name", "__filename", "__handle", "__continuation", "__acquired" ]

    def __init__(
        self,
        fp: IOBase,
        filename: str,
        name: str | None = None,
        continuation: Callable[[bool, IOBase, str], None] | None = None
    ):
        super().__init__()
        self.__name = name
        self.__filename = filename
        self.__handle: IOBase = fp
        self.__acquired = False
        self.__continuation = continuation

    @property
    def name(self) -> str | None:
        return self.__name

    @property
    def filename(self) -> str:
        return self.__filename

    def acquire(self):
        if self.finalized:
            raise FinalizedError

        org_pos = self.__handle.tell() or 0

        try:
            if org_pos:
                log.debug(f"Rewinding '{self.__filename}")
                self.__handle.seek(0)

            Handle.lock(self.__handle, self.__filename, self.__name)

            self.__acquired = True

        except:
            if self.__continuation:
                log.debug(f"Executing continuation on {self.__filename}")
                self.__continuation(False, self.__handle, self.__filename)

            raise
        finally:
            if org_pos:
                log.debug(f"Winding '{self.__filename} to pos {org_pos}")
                self.__handle.seek(org_pos)

    def release(self):
        if self.finalized:
            raise FinalizedError

        was_acquired = self.__acquired

        if self.__handle:
            try:
                if self.__acquired:
                    Handle.unlock(self.__handle, self.__filename, self.__name)
                    self.__acquired = False

                self.__handle.close()
            except Exception as ex: # pragma: no cover
                log.error(f"Unlocking {self.__filename} #{self.__handle.fileno()} failed: {ex}")

            if self.__continuation:
                log.debug(f"Executing continuation on {self.__filename}")
                self.__continuation(was_acquired, self.__handle, self.__filename)

    def __finalize__(self):
        self.__handle.close()
        self.__handle = None # pyright: ignore[reportAttributeAccessIssue]

    def __exit__(self, *args: Any):
        self.release()
        self.finalize()

    def __enter__(self):
        self.acquire()


    @staticmethod
    def lock(handle: IOBase, filename: str, name: str | None = None) -> None:
        if platform == "win32":
            try:
                log.info(f"Locking {filename} #{handle.fileno()}")
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except EnvironmentError as ex:
                if ex.errno == 13:
                    log.info(f"Locking {filename} #{handle.fileno()} failed")
                    raise LockException(name or filename)
                else:
                    log.error(f"Locking {filename} #{handle.fileno()} failed: {ex}")
                    raise

        else:
            try:
                log.info(f"Locking {filename} #{handle.fileno()}")
                fcntl.lockf(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except EnvironmentError:
                log.info(f"Locking {filename} #{handle.fileno()} failed")
                raise LockException(name or filename)

    @staticmethod
    def unlock(handle: IOBase, filename: str, name: str | None = None) -> None:
        try:
            if platform == "win32":
                log.info(f"Unlocking {filename} #{handle.fileno()}")
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                log.info(f"Unlocking {filename} #{handle.fileno()}")
                fcntl.lockf(handle, fcntl.LOCK_UN)
        except Exception as ex:
            log.error(f"Unlocking {filename} #{handle.fileno()} failed: {ex}")
            raise