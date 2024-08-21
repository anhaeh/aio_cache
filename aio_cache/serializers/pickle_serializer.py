import pickle
from typing import Any
from aio_cache.serializers import Serializer


class PickleSerializer(Serializer):
    @classmethod
    def encode(cls, value: Any) -> bytes:
        return pickle.dumps(value)

    @classmethod
    def decode(cls, value: str) -> Any:
        if value:
            value = pickle.loads(value)
        return value
