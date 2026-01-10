import time
from functools import lru_cache

@lru_cache(maxsize=512)
def cached_prediction(key):
    return None
