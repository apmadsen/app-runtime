from os import path, getlogin, getenv
from sys import platform
from re import split as rx_split
from getpass import getuser
from subprocess import run, DEVNULL, STDOUT , check_output
from importlib import import_module

from milieu.internal.app.compat import os, grp

if platform == "win32":
    pass
else:
    os = import_module("os")
    grp = import_module("grp")

def _get_user_id() -> int | None:
    if platform == "win32":
        return None
    else:
        return os.getuid()

def _get_username() -> str:
    for method in ( getlogin,
                    getuser,
                    lambda: getenv('username') ):
        try:
            if result := method():
                return result
        except:
            pass

    raise Exception("Unable to get username")

def _get_user_home() -> str:
    for method in ( lambda: path.expanduser("~"),
                    lambda: getenv('USERPROFILE') ):
        try:
            if result := method():
                return result
        except:
            pass

    raise Exception("Unable to get username")

def _get_user_roles() -> frozenset[str]:
    if platform == "win32":
        try:
            grps_str = rx_split("\r\n|\n", check_output("net localgroup", encoding = "cp437"))
            return frozenset([
                g.strip("*").lower()
                for g in grps_str
                if len(g) > 1
                 and g[0] == "*"
            ])
        except:
            raise
    else:
        try:
            return frozenset([
                g.gr_name.lower()
                for g in grp.getgrall()
                if USER_NAME in g.gr_mem
                 or g.gr_gid == USER_ID
            ])
        except:
            raise

def _get_is_elevated() -> bool:
    if platform == "win32":
        try:
            return run("net session", stdout = DEVNULL, stderr=STDOUT).returncode == 0
        except:
            return False
    else:
        try:
            return USER_ID == 0
        except:
            return False

USER_ID = _get_user_id()
USER_NAME = _get_username()
USER_HOME = _get_user_home()
USER_ROLES = _get_user_roles()
USER_ELEVATED = _get_is_elevated()


def get_username() -> str:
    """Returns the username of the current user.
    """
    return USER_NAME

def get_home() -> str:
    """Returns the home dir of the current user.
    """
    return USER_HOME

def get_roles() -> frozenset[str]:
    """Returns the roles of the current user.
    """
    return USER_ROLES

def is_in_role(role: str) -> bool:
    """
    Indicates if current user has the specified role.

    Args:
        role (str) The role (case insensitive)

    Returns:
        bool
    """
    return role.lower() in USER_ROLES

def is_elevated() -> bool:
    """Indicates if the current user has elevated administrative rights, i.e. running as admin in Windows or as sudo in Linux.
    """
    return USER_ELEVATED

is_admin = is_elevated