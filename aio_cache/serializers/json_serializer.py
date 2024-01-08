import orjson
from typing import Any
from aio_cache.serializers import Serializer


class JsonSerializer(Serializer):

    @classmethod
    def encode(cls, value: Any) -> bytes:
        return orjson.dumps(value, default=str)

    @classmethod
    def decode(cls, value: str) -> Any:
        if value:
            value = orjson.loads(value)
        return value
