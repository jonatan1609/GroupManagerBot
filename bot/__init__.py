from logging import getLogger, ERROR
getLogger("pyrogram.crypto.aes").setLevel(ERROR)

from pyrogram import Client
from pyrogram.session import Session
from dynaconf import Dynaconf
from os import environ


__version__ = "1.0.0"
Session.notice_displayed = True
futures = {}
config = Dynaconf(settings_files=[environ.get("config_file", "config.toml")])
strings = Dynaconf(settings_files=[".strings.toml"])
client = Client(**config.pyrogram)


def remove_future(future, key=None, ban_func: callable = None):
    del futures[key]
    if not future.done():
        client.loop.create_task(ban_func())
