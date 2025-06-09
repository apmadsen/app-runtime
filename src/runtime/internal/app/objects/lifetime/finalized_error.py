
class FinalizedError(BaseException):
    def __init__(self): # pragma: no cover
        super().__init__("Object is finalized")
