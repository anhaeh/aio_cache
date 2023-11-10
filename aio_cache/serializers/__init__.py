from abc import ABC, abstractmethod
from typing import Any


class Serializer(ABC):

    @classmethod
    @abstractmethod
    def encode(cls, value) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def decode(cls, value) -> Any:
        pass
