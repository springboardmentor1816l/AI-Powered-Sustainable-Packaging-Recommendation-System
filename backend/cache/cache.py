from extensions import cache

def make_cache_key(*args, **kwargs):
    return str(args) + str(kwargs)
