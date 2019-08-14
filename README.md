[![CircleCI](https://circleci.com/gh/o3o3o/django-fakeredis.svg?style=svg)](https://circleci.com/gh/o3o3o/django-fakeredis)

Easier use [fakeredis](https://pypi.org/project/fakeredis) in Django.


### Install

```
pip install django-fakeredis
```

## Why use it?

I have experienced many times to find bugs which is caused by mutiple fakeredis instances in tests.
We just want to use fakerredis like redis with one redis-server and different connections and can debug with MONITOR command in redis

### Features:

* One fakeredis server with mutiple connections for tests like the way of using redis. 
* Combine override settings to Local-memory and fake [get_redis_connection](https://github.com/niwinz/django-redis), [django's cache](https://docs.djangoproject.com/en/2.2/topics/cache/)
* To disable the fake action with passing env: "NOFAKE_REDIS=1"
  `NOFAKE_REDIS=1 python manage.py test`

Before you use `django_fakeredis`, your tests code maybe like that:

```python
server = fakeredis.FakeServer()
@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache" }})
@patch('foo.get_redis_connection', fakeredis.FakeRedis(server=server)
def test_sth():
    ....
```

Now your can just:
```python
@FakeRedis("yourpath.get_redis_connection")
def test_sth():
    ...
```



### Usage
```python

from django_fakeredis import FakeRedis
@FakeRedis("yourpath.get_redis_connection")
def test_foo():
    ...
```


```python
from django_fakeredis import FakeRedis
with FakeRedis("yourpath.get_redis_connection"):
    foo()
```

```python
from django_fakeredis import FakeRedis
with FakeRedis("yourpath.cache"):
    foo()
```

#### NOTE

1. If you want to mock `django.core.cache.cache` with fakeredis, django-fakeredis do nothing but just override CACHE settings into [Local-Memory](https://docs.djangoproject.com/en/2.2/topics/cache/#local-memory-caching) for using the internal cast. So there are two mocked redis instance for django.cache and get_redis_connection .

If you want to use more redis commands, such as: sets, list...,  you may need use [django_redis]((https://github.com/niwinz/django-redis)), and cast the result by hand.

django.cache:
```
from django.core.cache import cache
cache.set("key", 2)
assert cache.get("key") == 2
```

you have to cast by hand, when using fakeredis or django_redis directly, you have to cast by hand:

```
import fakeredis
con = fakeredis.FakeStrictRedis()
con.set("key", 2)
assert con.get("key").decode('utf8') == "2"
```

2. if you have a problem that mock is not worked, you may should to see [where to patch](https://docs.python.org/3/library/unittest.mock.html#where-to-patch)
