# pyright: basic
from os import path, remove
from typing import cast

from tests.testbase import TestBase

from milieu.user import get_home, get_roles, get_username, is_elevated, is_admin, is_in_role

class TestUser(TestBase):

    def test_get_username(self):
        username = get_username()
        self.assertGreater(len(username), 0)

    def test_get_home(self):
        username = get_username()
        homedir = get_home()
        self.assertTrue(username.lower() in homedir.lower())
        self.assertTrue(path.isdir(homedir))

    def test_get_roles(self):
        roles = get_roles()
        self.assertGreater(len(roles), 0)

    def test_is_elevated(self):
        result = is_elevated()
        self.assertFalse(result)
        self.assertEqual(is_admin, is_elevated)

    def test_is_in_role(self):
        roles = get_roles()
        for role in roles:
            self.assertTrue(is_in_role(role))


    def tearDown(self):
        pass
