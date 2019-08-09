from django.test import TestCase
from django_fakeredis import FakeRedis

# Mock path is 'django_fakeredis.tests.get_redis_connection'
from django_redis import get_redis_connection

# The mock path is 'django_fakeredis.tests.cache'
from django.core.cache import cache


class FakeRedisTestCase(TestCase):
    def test_fakeredis_with_get_redis_connnection(self):
        with FakeRedis("django_fakeredis.tests.get_redis_connection"):
            self.foo()

    def test_fakeredis_with_cache(self):
        with FakeRedis("django_fakeredis.tests.cache"):
            self.foo_cache()

    def foo(self):
        con = get_redis_connection()
        con.set("key", 1)
        self.assertEquals(con.get("key").decode("utf8"), "1")

        con2 = get_redis_connection()
        # now get value from the same server with different connection
        self.assertEquals(con2.get("key").decode("utf8"), "1")

    def foo_cache(self):
        cache.set("key", 2)
        # NOTE: There internal cast in django cache
        self.assertEquals(cache.get("key"), 2)
