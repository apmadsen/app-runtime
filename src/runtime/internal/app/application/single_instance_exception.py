class SingleInstanceException(Exception):
    def __init__(self): # pragma: no cover
        super().__init__("Another instance of application is already running...!")

