import redis.asyncio as redis
from typing import Any, Generator
from aio_cache.backends import BaseBackend


class RedisBackend(BaseBackend):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.__db = int(self._url.path[1:])
        except Exception:
            self.__db = 0

        self.__pool = redis.ConnectionPool(host=self._host, username=self._username, password=self._password,
                                           db=self.__db, protocol=3, max_connections=self._max_connections)
        self.__client = redis.Redis(connection_pool=self.__pool)

    async def set(self, key: str, value: Any, ttl: int = None):
        ttl = ttl or self._ttl
        k = self._prefix + key
        return await self.__client.set(k, self._serializer.encode(value), ex=ttl)

    async def get(self, key: str):
        k = self._prefix + key
        return self._serializer.decode(await self.__client.get(k))

    async def mget(self, keys: list) -> Generator:
        pipe = await self.__client.pipeline()
        for x in keys:
            pipe.get(self._prefix + x)
        results = await pipe.execute()
        return (self._serializer.decode(x) for x in results)

    async def mset(self, items: list[tuple[str, Any]], ttl: int = None):
        ttl = ttl or self._ttl
        pipe = await self.__client.pipeline()
        for k, v in items:
            pipe.set(self._prefix + k, self._serializer.encode(v), ttl)
        return await pipe.execute()

    async def delete_by_pattern(self, pattern: str):
        keys = await self.__client.keys(self._prefix + pattern + "*")
        if not keys:
            return 0
        return await self.__client.delete(*keys)

    async def close(self):
        await self.__client.aclose()
