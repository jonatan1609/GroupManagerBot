from logging import getLogger, ERROR
getLogger("pyrogram.crypto.aes").setLevel(ERROR)

from pyrogram import Client, types
from pyrogram.session import Session
from dynaconf import Dynaconf
from os import environ
from loguru import logger
from .cache import Cache


__version__ = "1.0.12"
Session.notice_displayed = True
futures = {}
logger.info(f'Loading config file from '
            f'{environ.get("CONFIG_FILE", "config.toml")!r}')
config = Dynaconf(settings_files=[environ.get("CONFIG_FILE", "config.toml")])
logger.info("Loading strings file from 'strings.toml'")
strings = Dynaconf(settings_files=["strings.toml"])
logger.info("Initializing Pyrogram client")
client = Client(**config.pyrogram)
cache = Cache(
    60 * 60 * 24,
    admins=Cache(60 * 60 * 24),
    names=Cache(60 * 60 * 24),
    permissions=Cache(60 * 60 * 24 * 2)
)
banned_permissions = types.ChatPermissions()


def remove_future(future, key=None, ban_func: callable = None):
    if futures.get(key):
        del futures[key]
    client.loop.create_task(client.delete_messages(key[0], key[-1]))
    if (future.done() and not future.result()) or not future.done():
        logger.info(f"Banning user {key[1]}")
        client.loop.create_task(ban_func())
    elif future.done() and future.result():
        logger.info(f"Removing restriction for user {key[1]}")
        client.loop.create_task(
            client.restrict_chat_member(
                key[0],
                key[1],
                cache["permissions"][key[0]]
            )
        )
