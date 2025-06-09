import sys
from os import getenv, path, remove
from typing import ContextManager, Any
from io import IOBase
from platformdirs import site_data_dir, user_data_dir

from runtime.core.user import is_elevated
from runtime.core.locking.handle import Handle
from runtime.core.locking.log import log

def lock_file(file_path: str) -> ContextManager[Any]:
    """Returns a Handle object for specified file_path."""
    log.debug(f"Creating a handle for {file_path}")
    return Handle(open(file_path, 'w'), file_path)

def lock_handle(name: str) -> ContextManager[Any]:
    """Returns a named Handle object in the common system path for shared locks."""
    file_path = get_shared_lock_path(name)

    if path.exists(file_path):
        log.error(f"Cannot create a handle for {file_path} because it already exists")
        raise FileExistsError(file_path)

    def cleanup(acquired: bool, handle: IOBase, filename: str):
        if acquired:
            log.debug(f"Cleaning up handle by disposing of {filename}")
            remove(filename)

    return Handle(open(file_path, 'w'), file_path, name, continuation = cleanup)

def get_shared_lock_path(name: str) -> str:
    """Returns the common system path for locks."""
    command = path.basename(sys.argv[0].split(" ", maxsplit = 1)[0])
    site_path = site_data_dir()
    user_path = user_data_dir()
    elevated = is_elevated()

    if sys.platform == "linux" and elevated: # pragma: no cover
        file_path = f"/var/run/{command}_{name}.pid"
    elif sys.platform == "win32" and elevated: # pragma: no cover
        file_path = path.join(site_path, f"{command}_{name}.lock")
    elif sys.platform == "win32": # pragma: no cover
        appdata_path = getenv("APPDATA", user_path)
        file_path = path.join(appdata_path, f"{command}_{name}.lock")
    else: # pragma: no cover
        file_path = path.join(user_path, f"{command}_{name}.lock")

    return file_path