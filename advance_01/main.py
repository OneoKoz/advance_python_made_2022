from lru_cache import LRUCache

cache = LRUCache(2)

cache.set("k1", "val1")
cache.set("k2", "val2")

cache.get("k3")
cache.get("k2")
cache.get("k1")

cache.set("k3", "val3")

cache.get("k3")
cache.get("k2")
cache.get("k1")

cache = LRUCache(2)

cache.set("k1", "val1")
cache.set("k2", "val2")
cache.set("k1", "val3")
cache.set("k4", "val4")

cache.get("k4")
cache.get("k2")
cache.get("k1")

cache.set("k4", "test")
cache.set("k5", "val5")

cache.get("k1")
cache.get("k2")
cache.get("k4")
cache.get("k5")

cache = LRUCache(0)
cache.set("k1", "val1")
cache.set("k2", "val2")

cache.get("k1")
cache.get("k2")
