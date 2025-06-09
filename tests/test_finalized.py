# pyright: basic
from os import path

from tests.testbase import TestBase

from milieu.objects.lifetime import Finalizable, FinalizedError

class TestFinalized(TestBase):

    def test_finalizable(self):
        class Test(Finalizable):
            _is_finalized = False

            def __finalize__(self) -> None:
                self._is_finalized = True

        t = Test()

        self.assertFalse(t.finalized)
        self.assertFalse(t._is_finalized)

        t.finalize()

        self.assertTrue(t.finalized)
        self.assertTrue(t._is_finalized)

        self.assertRaises(FinalizedError, t.finalize)

    def tearDown(self):
        pass


