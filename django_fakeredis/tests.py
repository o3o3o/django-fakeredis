from django.test import TestCase
from django_fakeredis import FakeRedis
from django_redis import get_redis_connection

from django.core.cache import cache


def foo():
    con = get_redis_connection()
    con.set("key", 1)
    assert con.get("key").decode("utf8") == "1"

    con2 = get_redis_connection()
    # now get value from the same server with different connection
    assert con2.get("key").decode("utf8") == "1"


def foo_cache():
    cache.set("key", 2)
    # NOTE: There internal cast in django cache
    try:
        assert cache.get("key").decode("utf8") == "2"
    except AttributeError:
        assert cache.get("key") == 2


class FakeRedisTestCase(TestCase):
    def test_fakeredis_with_get_redis_connnection(self):
        with FakeRedis("django_fakeredis.tests.get_redis_connection"):
            foo()

    def test_fakeredis_with_cache(self):
        with FakeRedis("django_fakeredis.tests.cache"):
            foo_cache()
