import asyncio
import pytest
import pytest_asyncio
from tests.fixtures import cache_service


@pytest_asyncio.fixture
async def memory_cache(cache_service):
    cache_service.initialize("memory://dummy/0")
    await cache_service.prune()
    yield cache_service


class TestMemoryBackend:

    @pytest.mark.asyncio
    async def test_set(self, memory_cache):
        await memory_cache.set("my_key", 123)
        result = await memory_cache.get("my_key")
        assert result == 123

    @pytest.mark.asyncio
    async def test_ttl(self, memory_cache):
        await memory_cache.set("my_key", "test", 1)
        await asyncio.sleep(1)
        result = await memory_cache.get("my_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_mset(self, memory_cache):
        await memory_cache.mset([("key1", 1), ("key2", 2)])
        results = await memory_cache.mget(["key1", "key2"])
        results = list(results)
        assert len(results) == 2
        assert results == [1, 2]

    @pytest.mark.asyncio
    async def test_delete(self, memory_cache):
        await memory_cache.set("my_app", "res")
        await memory_cache.delete_by_pattern("my_")
        result = await memory_cache.get("my_app")
        assert result is None
