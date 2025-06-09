from os import isatty, path, getenv
import sys
from types import ModuleType
from typing import ContextManager, Any, cast
from importlib.metadata import Distribution, distributions, distribution

from runtime.core.locking.lock_exception import LockException
from runtime.core.application.single_instance_exception import SingleInstanceException
from runtime.core.locking import lock_handle
from runtime.core.user import is_elevated, get_home

MAIN_MODULE = sys.modules["__main__"]
SINGLE_INSTANCE_FILENAME = "singleinstance"
IS_ELEVATED = is_elevated()

def get_main_module() -> ModuleType:
    """Returns the main module.
    """
    return MAIN_MODULE

def get_main_package() -> Distribution:
    """Returns the main module package.
    """
    return distribution(getattr(MAIN_MODULE, "__package__"))

def get_auxilary_packages() -> dict[str, Distribution]:
    """Returns all installed packages (except for main package).
    """
    mp = getattr(MAIN_MODULE, "__package__") or get_main_package().name
    return {
        dist.name: dist
        for dist in distributions()
        if dist.name != mp
    }

def get_application_path() -> str:
    """Returns the path of the main module.

    Raises:
        Exception: An exception is raised, if application is running in a python shell.
    """
    if hasattr(MAIN_MODULE, "__file__"):
        return getattr(MAIN_MODULE, "__file__")
    else:
        raise Exception("Unable to get application path when running in a python shell") # pragma: no cover

def is_interactive() -> bool:
    """Indicates if application is running inside a terminal or not.
    """
    try:
        return isatty(sys.stdout.fileno())
    except: # pragma: no cover
        return False

def is_python_shell() -> bool:
    """Indicates if application is running inside a python shell or not.
    """
    return not hasattr(MAIN_MODULE, "__file__")

def single_instance() -> ContextManager[Any]:
    """
    Returns a SingleInstance context, which ensures that application is only running in one instance.
    """
    try:
        return lock_handle(SINGLE_INSTANCE_FILENAME)
    except LockException: # pragma: no cover
        raise SingleInstanceException

def get_installalled_apps_path(elevated: bool = IS_ELEVATED) -> str: # pragma: no cover
    """Gets the default path for installed user applications."""
    if elevated:
        if sys.platform == "win32":
            if result := (getenv("ProgramFiles") or
                          getenv("ProgramFiles(x86)") or
                          getenv("ProgramW6432")):

                return path.abspath(result)
        elif sys.platform == "linux":
            if path.isdir("/usr/local/bin"):
                return "/usr/local/bin"
    else:
        if sys.platform == "win32":
            if result := getenv("LocalAppData"):
                return path.abspath(path.join(result, "Programs"))
        elif sys.platform == "linux":
            if ( home := get_home() ) and ( local := path.join(home, ".local") ) and path.isdir(local):
                return local

    raise FileNotFoundError

