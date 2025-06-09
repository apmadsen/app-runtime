# pyright: basic
from typing import Any
from sys import stdout
from os import path, makedirs, remove, get_terminal_size
from shutil import rmtree
from unittest import TestCase, main
from logging import Logger, Handler, FileHandler, StreamHandler, Formatter, DEBUG
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

class TestBase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if cls.__name__.upper() in ("TEST", "TESTCASE"):
            raise Exception(f"""Test class name cannot be just "{cls.__name__}"!""")

        cls._base_dir = path.join("tests/testdata", cls.__name__)
        # cls._logs_dir = path.join("tests/logs")

        if path.isdir(cls._base_dir):
            rmtree(cls._base_dir)

        makedirs(cls._base_dir)
        # if not path.isdir(cls._logs_dir):
        #     makedirs(cls._logs_dir)

    @classmethod
    def tearDownClass(cls):
        if path.isdir(cls._base_dir):
            rmtree(cls._base_dir)

        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.test_dir = path.join(self._base_dir, self._testMethodName)
        makedirs(self.test_dir)

        # logpath = path.join(self._logs_dir, type(self).__name__, f"{self._testMethodName}.log")

        # try:
        #     if path.isfile(logpath):
        #         remove(logpath)
        # except:
        #     pass

        # if not path.isdir(path.dirname(logpath)):
        #     makedirs(path.dirname(logpath))

        # self._test_log_file_handler = FileHandler(logpath)
        self._test_log_stream_handler = StreamHandler()

        self._test_log_queue: Queue[Any] = Queue()
        self._test_log_queue_listener = QueueListener(
            self._test_log_queue,
            # self._test_log_file_handler,
            self._test_log_stream_handler
        )
        self._test_log_queue_listener.start()
        self.test_log_handler = QueueHandler(self._test_log_queue)
        self.test_log_handler.setFormatter(Formatter("%(asctime)s [%(process)d-%(threadName)s] %(levelname)s: %(message)s"))
        self.test_log = Logger(self.id(), level = DEBUG)
        self.test_log.addHandler(self.test_log_handler)
        self.test_log_unformatted = Logger(self.id())
        # self.test_log_unformatted.addHandler(self._test_log_file_handler)
        self.test_log_unformatted.addHandler(self._test_log_stream_handler)

        self.terminal_size = 50
        stdout.write("\n")
        self.test_log_unformatted.info("-" * self.terminal_size)
        self.test_log_unformatted.info(f"Setting up test {self.id()}")

    def tearDown(self):
        self.test_log.info(f"Ending test {self.id()}")
        self.test_log_handler.flush()
        self.test_log_handler.close()
        self._test_log_queue_listener.stop()
        # self._test_log_file_handler.flush()
        # self._test_log_file_handler.close()
        self._test_log_stream_handler.flush()
        self._test_log_stream_handler.close()

        try:
            if path.isdir(self.test_dir):
                rmtree(self.test_dir)
        except:
            pass

        super().tearDown()

