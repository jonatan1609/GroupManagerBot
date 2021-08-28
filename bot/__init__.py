from logging import getLogger, ERROR
getLogger("pyrogram.crypto.aes").setLevel(ERROR)

from pyrogram import Client
from pyrogram.session import Session
from dynaconf import Dynaconf
from os import environ
from .cache import Cache


__version__ = "1.0.6"
Session.notice_displayed = True
futures = {}
config = Dynaconf(settings_files=[environ.get("CONFIG_FILE", "config.toml")])
strings = Dynaconf(settings_files=["strings.toml"])
client = Client(**config.pyrogram)
cache = Cache(60 * 60 * 24, admins=Cache(60 * 60 * 24), names=Cache(60 * 60 * 24))


def remove_future(future, key=None, ban_func: callable = None):
    if futures.get(key):
        del futures[key]
    client.loop.create_task(client.delete_messages(key[0], key[-1]))
    if (future.done() and not future.result()) or not future.done():
        client.loop.create_task(ban_func())
