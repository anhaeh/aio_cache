# Aio-Cache (asyncio cache)
Python cache library for use with asyncio. This including retries (tenacity), exponential backoff and serialization.
It is possible add more backends and serializers easily.
Require Python 3.10+


## Available Backends
* Memory
* Redis (https://github.com/redis/redis-py)

## Available Serializers
* msgpack (default)
* orjson


### Null Backend
Null Cache is the default backend. Your app will run without cache.
``` python
from aio_cache.cache_service import CacheService

cache = CacheService()
await cache.set("hello", "world")
```


### Redis backend
``` python
from aio_cache.cache_service import CacheService

cache = CacheService()
cache.initialize(cache_uri="redis://localhost/0?ttl=60", prefix="my_prefix")

await cache.set("hello", [1, 2, 3])
await cache.get("hello")
```

### Memory backend
``` python
from aio_cache.cache_service import CacheService

cache = CacheService()
cache.initialize(cache_uri="memory://")
await cache.set("hello", "world", ttl=60)
```

### Another serializer
``` python
from aio_cache.cache_service import CacheService

cache = CacheService()
cache.initialize(cache_uri="memory://", serializer="json")
await cache.set("hello", "world")
```

## Exceptions
You can define a custom exception for handle when an error appears
```python
class CustomCacheException(Exception):
    pass

cache = CacheService(cache_error_exception=CustomCacheException)
```


## Unit Tests
```bash
pip install -r dev.reqs.txt
pytest
# with coverage
sh ./run_tests.sh
```

