from abc import ABC, abstractmethod
from typing import Any
from urllib.parse import parse_qs, ParseResult
from aio_cache.serializers import Serializer


class BaseBackend(ABC):
    def __init__(self, url: ParseResult, prefix: str, serializer: Serializer):
        self._url: ParseResult = url
        self._prefix: str = prefix
        self._query = parse_qs(url.query)
        self._ttl = int(self._query.get("ttl", [60 * 60])[0])
        self._max_connections = int(self._query.get("max_connections", [50])[0])
        self._host: str = url.hostname
        self._password: str = url.password
        self._username: str = url.username

        self._serializer = serializer

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int = None):
        pass

    @abstractmethod
    async def get(self, key: str):
        pass

    @abstractmethod
    async def delete_by_pattern(self, pattern: str):
        pass

    @abstractmethod
    async def mget(self, keys: list[Any]):
        pass

    @abstractmethod
    async def mset(self, items: list[tuple[str, Any]], ttl: int = None):
        pass

    async def close(self):
        pass

    async def prune(self):
        pass
