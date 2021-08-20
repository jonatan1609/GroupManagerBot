from pyrogram import Client, types
from ..filters import human, bot
from .. import futures, strings


@Client.on_callback_query(human)
async def i_am_a_human(client: Client, callback: types.CallbackQuery):
    future = futures.get((callback.message.chat.id, callback.from_user.id))
    if future:
        future.set_result(True)
        await callback.message.edit_text(strings.hebrew.welcome)
        client.loop.call_later(3, lambda: client.loop.create_task(callback.message.delete()))
    else:
        await callback.answer(strings.hebrew.message_not_for_you)


@Client.on_callback_query(bot)
async def i_am_a_bot(client: Client, callback: types.CallbackQuery):
    future = futures.get((callback.message.chat.id, callback.from_user.id))
    if future:
        future.set_result(False)
        await callback.message.edit_text(strings.hebrew.bye)
        await callback.message.chat.kick_member(callback.from_user.id, 3000)
        client.loop.call_later(3, lambda: client.loop.create_task(callback.message.delete()))
    else:
        await callback.answer(strings.hebrew.message_not_for_you)
