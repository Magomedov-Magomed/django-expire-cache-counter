import time
from collections import defaultdict

from django.core.cache.backends.redis import RedisCache


class ExpireCacheCounter:
    def __init__(self, _cache: RedisCache, ttl=1):
        self.store = defaultdict(list)
        self.__ttl = ttl
        self.cache = _cache

    def __setitem__(self, key, value):
        if from_cache := self.cache.get(key):
            self.store[key] = from_cache
        self.store[key].append(time.time())
        self.cache.set(key, self.store[key])

    def __getitem__(self, item):
        if from_cache := self.cache.get(item):
            self.store[item] = from_cache
        self.store[item] = [i for i in self.store[item] if time.time() - i < self.__ttl]
        self.cache.set(item, self.store[item])
        return len(self.store[item])
