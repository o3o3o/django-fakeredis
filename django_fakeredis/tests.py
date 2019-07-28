from django.test import TestCase
from django_fakeredis.fakeredis import FakeRedis
from django_redis import get_redis_connection


def foo():
    con = get_redis_connection()
    con.set("key", 1)
    assert con.get("key").decode("utf8") == "1"

    con2 = get_redis_connection()
    # now get value from the same server with different connection
    assert con2.get("key").decode("utf8") == "1"


class FakeRedisTestCase(TestCase):
    def test_fakeredis(self):
        with FakeRedis("django_fakeredis.tests.get_redis_connection"):
            foo()
