import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):

    def test_set_get(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "val1")

    def test_set_get_change(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k1", "val3")
        cache.set("k4", "val4")

        self.assertEqual(cache.get("k4"), "val4")
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "val3")

        cache.set("k4", "test")
        cache.set("k5", "val5")

        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k4"), "test")
        self.assertEqual(cache.get("k5"), "val5")

    def test_set_get_zero_limit(self):
        cache = LRUCache(0)
        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), "val2")
