from pyrogram import Client, types
from ..filters import human, bot
from .. import futures, strings
from ..database import Group
from pony.orm import db_session
from loguru import logger


@Client.on_callback_query(human)
async def i_am_a_human(_: Client, callback: types.CallbackQuery):
    future = futures.get(
        (
            callback.message.chat.id,
            callback.from_user.id,
            callback.message.message_id
        )
    )
    with db_session:
        group = Group.get(id=callback.message.chat.id)
        if not group:
            logger.error(f"Group {callback.message.chat.id} not found!")
    if future:
        future.set_result(True)
    else:
        await callback.answer(
            getattr(strings, group.default_language).message_not_for_you
        )


@Client.on_callback_query(bot)
async def i_am_a_bot(_: Client, callback: types.CallbackQuery):
    future = futures.get(
        (
            callback.message.chat.id,
            callback.from_user.id,
            callback.message.message_id
        )
    )
    with db_session:
        group = Group.get(id=callback.message.chat.id)
        if not group:
            logger.error(f"Group {callback.message.chat.id} not found!")
    if future:
        future.set_result(False)
    else:
        await callback.answer(
            getattr(strings, group.default_language).message_not_for_you
        )
