import os
import fakeredis
from unittest.mock import patch
from django.test import override_settings

server = fakeredis.FakeServer()


def get_fake_redis():
    """ mock the same redis connection """
    return fakeredis.FakeStrictRedis(server=server)


class FakeRedis:
    """
    Combine override settings:  CACHE and  fakeredis
    To disable the fake action with passing env: "NOFAKE_REDIS=1"
    """

    NOFAKE_REDIS = True if "NOFAKE_REDIS" in os.environ else False

    def __init__(self, path):
        self.path = path
        self.override_settings = None
        self.patch = None

        if not self.NOFAKE_REDIS:
            self.override_settings = override_settings(
                CACHES={
                    "default": {
                        "BACKEND": "django.core.cache.backends.dummy.DummyCache"
                    }
                }
            )
            self.patch = patch(self.path, get_fake_redis)

    def __call__(self, fn):
        if not self.NOFAKE_REDIS:
            fn = self.override_settings(fn)
            fn = self.patch(fn)

        return fn

    def __enter__(self):
        if not self.NOFAKE_REDIS:
            return self.override_settings.__enter__(), self.patch.__enter__()
        return None, None

    def __exit__(self, *args, **kw):
        if not self.NOFAKE_REDIS:
            self.override_settings.__exit__(*args, **kw)
            self.patch.__exit__(*args, **kw)
