from asyncio import get_running_loop, get_event_loop
from functools import partial
from loguru import logger
from .utils import shorten


class Cache(dict):
    def __init__(self, default_time, loop=None, *args, **kwargs):
        if not loop:
            try:
                loop = get_running_loop()
            except RuntimeError:
                loop = get_event_loop()
        self.loop = loop
        self.default_time = default_time
        super().__init__(*args, **kwargs)

    def insert(self, key, value, ttl: int = -1):
        if ttl == -1:
            ttl = self.default_time

        self[key] = value
        logger.info(f"Key - {shorten(key)!r}, "
                    f"Value - {shorten(value)!r} "
                    f"was inserted to cache for {ttl} seconds")
        self.loop.call_later(ttl, partial(self.delete, key))

    def delete(self, key):
        del self[key]
        logger.info(f"Key - {shorten(key)!r} was deleted from cache")
