from typing import Any
from time import time
from datetime import datetime, timedelta
from aio_cache.backends import BaseBackend


class MemoryBackend(BaseBackend):
    def __init__(self, *args, **kwargs):
        self._cache = {}
        super().__init__(*args, **kwargs)

    async def set(self, key: str, value: Any, ttl: int = None):
        ttl = ttl or self._ttl
        due_time = datetime.now() + timedelta(seconds=ttl or self._ttl)
        due_time = float(due_time.strftime("%s"))
        self._cache[key] = (value, due_time)

    async def get(self, key: str):
        value, due = self._cache.get(key, (None, 0))
        if value is not None and time() > due:
            value = None
            del self._cache[key]
        return value

    async def delete_by_pattern(self, pattern: str):
        to_delete = []
        for key in self._cache:
            if key[:len(pattern)] == pattern:
                to_delete.append(key)
        for x in to_delete:
            del self._cache[x]

    async def mget(self, keys: list):
        return [await self.get(key) for key in keys]

    async def mset(self, items: list[tuple[str, Any]], ttl: int = None):
        for k, v in items:
            await self.set(k, v, ttl)

    async def prune(self):
        self._cache = {}



