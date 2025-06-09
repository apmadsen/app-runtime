class LockException(Exception):
    def __init__(self, handle: str):
        super().__init__(f"Handle {handle} is already locked by another instance of this application...!")
