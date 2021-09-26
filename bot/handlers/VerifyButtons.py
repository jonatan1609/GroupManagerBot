from pyrogram import Client, types, errors
from ..filters import human, bot
from .. import futures, strings
from ..database import Group
from pony.orm import db_session
from loguru import logger


async def get_future(client, callback):
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
            try:
                await client.send_message(
                    callback.message.chat.id,
                    strings.readd_group
                )
            except errors.RPCError as e:
                logger.error(e.MESSAGE)
            try:
                await callback.message.chat.leave()
            except errors.RPCError as e:
                logger.error(e.MESSAGE)
    return future, group


@Client.on_callback_query(human)
async def i_am_a_human(client: Client, callback: types.CallbackQuery):
    future, *group = await get_future(client, callback)
    group, = group
    if not group:
        return
    if future:
        future.set_result(True)
    else:
        await callback.answer(
            getattr(strings, group.default_language).message_not_for_you
        )


@Client.on_callback_query(bot)
async def i_am_a_bot(client: Client, callback: types.CallbackQuery):
    future, *group = await get_future(client, callback)
    group, = group
    if not group:
        return
    if future:
        future.set_result(False)
    else:
        await callback.answer(
            getattr(strings, group.default_language).message_not_for_you
        )
