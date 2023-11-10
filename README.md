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
result = await cache.get("hello")

await cache.mset("hello", [("key1", 1), ("key2": "bye")]) # multi set using a pipeline
results = await cache.mget("hello", ["key1", "key2"]) # multi get using a pipeline

await cache.delete_by_pattern("key") # delete keys thats match with "key*"
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


## Fast-Api integration sample
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aio_cache.cache_service import CacheService


class RedisException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()

cache = CacheService(cache_error_exception=RedisException)
cache.initialize(cache_uri="redis://localhost/0", prefix="fast_")


@app.exception_handler(RedisException)
async def redis_exception_handler(request: Request, exc: RedisException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name}. Maybe you must to check your redis..."},
    )


@app.get("/cache/{name}/")
async def read_name(name: str):
    result = await cache.get(name)
    return {"result": result}
```

