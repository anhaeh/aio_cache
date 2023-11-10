from typing import Any
from urllib.parse import urlparse
from importlib import import_module

from tenacity import retry, stop_after_delay, stop_after_attempt, wait_random_exponential

from aio_cache.backends.null_backend import NullBackend
from aio_cache.utils import Singleton


class InvalidModuleAioCacheException(Exception):
    pass


def safe(f):
    @retry(reraise=True, stop=(stop_after_delay(25) | stop_after_attempt(3)),
           wait=wait_random_exponential(multiplier=2, max=10))
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except Exception as e:
            exception = args[0].cache_error_exception or Exception
            raise exception(repr(e))

    return wrapper


class CacheService(metaclass=Singleton):
    BACKENDS = [
        "redis",
        "memory"
    ]

    SERIALIZERS = [
        "msgpack",
        "json"
    ]

    def __init__(self, cache_error_exception=None):
        self.__backend = NullBackend()
        self.cache_error_exception = cache_error_exception

    @staticmethod
    def __import_module(name, available_modules: list, module_path: str):
        if name not in available_modules:
            raise InvalidModuleAioCacheException(f"[aio_cache] Unknown module {name}. Available: {available_modules}")
        return import_module(module_path.format(name))

    def __get_backend_class(self, url_parsed):
        backend_name = url_parsed.scheme
        m = self.__import_module(backend_name, self.BACKENDS, "aio_cache.backends.{}_backend")
        return getattr(m, f"{backend_name.title()}Backend")

    def __get_serializer_class(self, name):
        m = self.__import_module(name, self.SERIALIZERS, "aio_cache.serializers.{}_serializer")
        return getattr(m, f"{name.title()}Serializer")

    def initialize(self, cache_uri: str = "", prefix: str = "", serializer: str = "msgpack"):
        self.__backend = NullBackend()

        if cache_uri:
            url_parsed = urlparse(cache_uri)
            backend_class = self.__get_backend_class(url_parsed)
            serializer_class = self.__get_serializer_class(serializer)
            self.__backend = backend_class(url_parsed, prefix, serializer_class)
        print(f"[aio_cache] {self.__backend.__class__.__name__} enabled")

    @safe
    async def set(self, key: str, value: Any, ttl: int = None):
        return await self.__backend.set(key, value, ttl)

    @safe
    async def get(self, key: str):
        return await self.__backend.get(key)

    @safe
    async def delete_by_pattern(self, pattern: str):
        return await self.__backend.delete_by_pattern(pattern)

    @safe
    async def mget(self, keys: list[Any]):
        return await self.__backend.mget(keys)

    @safe
    async def mset(self, items: list[tuple[str, Any]], ttl: int = None):
        return await self.__backend.mset(items, ttl)

    @safe
    async def close(self):
        return await self.__backend.close()

    @safe
    async def prune(self):
        return await self.__backend.prune()

# samples
# uri_memory = "memory://dummy"
# uri_redis = "redis://:master@10.0.3.136/1?ttl=120"
