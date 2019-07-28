[![CircleCI](https://circleci.com/gh/o3o3o/django-fakeredis.svg?style=svg)](https://circleci.com/gh/o3o3o/django-fakeredis)

More easier to use [fakeredis](https://pypi.org/project/fakeredis) in django.


### Install

```
pip install django-fakeredis
```

## Why use it?

I have experienced many times to find bugs which is caused by mutiple fakeredis instances in tests.
We just want to use fakerredis like redis with one redis-server and different connections.

### Pros:

* One fakeredis server with mutiple connections for tests like the way of using redis. 
* Combine override settings to DummyCACHE and fake get_redis_connection
* To disable the fake action with passing env: "NOFAKE_REDIS=1"
  `NOFAKE_REDIS=1 python manage.py test`

Before you use `django_fakeredis`, your everty test code maybe like that:

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

from django_fakeredis.fakeredis import FakeRedis
@FakeRedis("yourpath.get_redis_connection")
def test_foo():
    ...
```


```python
from django_fakeredis.fakeredis import FakeRedis
with FakeRedis("yourpath.get_redis_connection"):
    foo()
```