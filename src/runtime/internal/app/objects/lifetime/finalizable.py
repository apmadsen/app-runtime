from typing import Any
from abc import ABC, abstractmethod
from weakref import finalize

from milieu.internal.app.objects.lifetime.finalized_error import FinalizedError

class Finalizable(ABC):
    __slots__ = [ "__weakref__", "__finalizer" ]

    def __new__(cls, *args: Any, **kwargs: Any):
        instance = super().__new__(cls)
        instance.__finalizer = finalize(instance, instance.__finalize__)
        return instance

    @property
    def finalized(self) -> bool:
        return not self.__finalizer.alive

    def finalize(self):
        if not self.__finalizer.alive:
            raise FinalizedError

        self.__finalizer()

    @abstractmethod
    def __finalize__(self) -> None:
        ... # pragma: no cover
