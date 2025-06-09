class TerminateException(Exception):
    def __init__(self): # pragma: no cover
        super().__init__("Application requested to terminate")

