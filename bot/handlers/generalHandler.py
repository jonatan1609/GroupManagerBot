from pyrogram import Client, types
from ..filters import private
from ..utils import shorten
from typing import Union
from loguru import logger


@Client.on_message(private, group=-1)
@Client.on_callback_query(group=-1)
async def handler(_: Client, update: Union[types.Message, types.CallbackQuery]):
    if isinstance(update, types.Message):
        message = f"User {update.from_user.id} sent {shorten(update.text)!r} to the bot"
    else:
        message = f"User {update.from_user.id} clicked a button {shorten(update.data)!r}"
    logger.info(message)
