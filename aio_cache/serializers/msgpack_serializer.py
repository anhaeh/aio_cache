import msgpack
from typing import Any
from aio_cache.serializers import Serializer


class MsgpackSerializer(Serializer):
    @classmethod
    def encode(cls, value: Any) -> bytes:
        return msgpack.dumps(value, default=str)

    @classmethod
    def decode(cls, value: str) -> Any:
        if value:
            value = msgpack.loads(value)
        return value
