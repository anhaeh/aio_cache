import asyncio
import pytest
from tests.fixtures import cache_service


@pytest.fixture
def redis_cache(cache_service):
    cache_service.initialize("redis://localhost/0")
    return cache_service


class TestRedisBackend:

    @pytest.mark.asyncio
    async def test_set(self, redis_cache):
        await redis_cache.set("my_key", 123)
        result = await redis_cache.get("my_key")
        assert result == 123

    @pytest.mark.asyncio
    async def test_ttl(self, redis_cache):
        await redis_cache.set("my_key", {"hello": "world"}, 1)
        await asyncio.sleep(1)
        result = await redis_cache.get("my_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_json(self, cache_service):
        cache_service.initialize("redis://localhost/0", prefix="json_app", serializer='json')
        await cache_service.set("my_key", [1, 2, 3])
        result = await cache_service.get("my_key")
        assert result == [1, 2, 3]

    @pytest.mark.asyncio
    async def test_mset(self, redis_cache):
        await redis_cache.mset([("key1", 1), ("key2", {"hello": "world"})])
        results = await redis_cache.mget(["key1", "key2"])
        results = list(results)
        assert len(results) == 2
        assert results == [1, {"hello": "world"}]

    @pytest.mark.asyncio
    async def test_delete(self, redis_cache):
        await redis_cache.set("my_app", "res")
        await redis_cache.delete_by_pattern("my_")
        result = await redis_cache.get("my_app")
        assert result is None
