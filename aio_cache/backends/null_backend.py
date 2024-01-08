from typing import Any, Sequence

from aio_cache.backends import BaseBackend


class NullBackend(BaseBackend):
    def __init__(self):
        pass

    async def set(self, key: str, value: Any, ttl: int = None):
        pass

    async def get(self, key: str):
        return None

    async def delete_by_pattern(self, pattern: str):
        return 0

    async def mget(self, keys: Sequence[str]):
        return [None for _ in keys]

    async def mset(self, items: Sequence[tuple[str, Any]], ttl: int = None):
        pass
