from flask_caching import Cache

cache = Cache(config={
    "CACHE_TYPE": "SimpleCache",   # In-memory
    "CACHE_DEFAULT_TIMEOUT": 300   # 5 minutes
})
