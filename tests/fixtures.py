import pytest
from aio_cache.cache_service import CacheService


class CustomCacheException(Exception):
    pass


@pytest.fixture
def cache_service():
    yield CacheService(cache_error_exception=CustomCacheException)
