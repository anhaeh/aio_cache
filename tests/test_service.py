import pytest
from unittest.mock import patch

from tests.fixtures import cache_service, CustomCacheException
from aio_cache.cache_service import InvalidModuleAioCacheException


class TestService:

    def test_invalid_backend(self, cache_service):
        with pytest.raises(InvalidModuleAioCacheException):
            cache_service.initialize("fake://localhost/0")

    def test_invalid_serializer(self, cache_service):
        with pytest.raises(InvalidModuleAioCacheException):
            cache_service.initialize("redis://localhost/0", serializer="fake")

    @pytest.mark.asyncio
    async def test_retrying(self, cache_service, caplog):
        with patch('aio_cache.backends.null_backend.NullBackend.set', side_effect=Exception("connection error")):
            with pytest.raises(CustomCacheException):
                await cache_service.set("test", 1)

