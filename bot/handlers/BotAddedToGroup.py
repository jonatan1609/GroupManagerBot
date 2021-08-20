from pyrogram import Client, types
from ..filters import group
from asyncio import Future
from .. import futures, remove_future, strings, config
from random import sample


@Client.on_chat_member_updated(group)
async def member_has_joined(client: Client, member: types.ChatMemberUpdated):
    if (
            member.new_chat_member
            and member.new_chat_member.status not in {"kicked", "left", "restricted"}
            and not member.old_chat_member
    ):
        if member.new_chat_member.user.is_self:
            return await client.send_message(
                member.chat.id,
                strings.hebrew.bot_was_added,
                reply_markup=types.InlineKeyboardMarkup([
                    [types.InlineKeyboardButton(strings.hebrew.button_config, url=f"t.me/{config.bot.username}?start={member.chat.id}")]
                ])
            )
        if message := await client.send_message(
            member.chat.id, strings.hebrew.welcome_to_the_group.format(
                f"[{member.new_chat_member.user.first_name}](tg://user?id={member.new_chat_member.user.id})"
            ), reply_markup=types.InlineKeyboardMarkup([
                    *sample([
                        [types.InlineKeyboardButton(strings.hebrew.i_am_a_bot, callback_data="bot")],
                        [types.InlineKeyboardButton(strings.hebrew.i_am_a_human, callback_data="human")]
                    ], 2)
                ])
        ):
            future = Future()
            callback = lambda *_: remove_future(
                future,
                (
                    member.chat.id, member.new_chat_member.user.id, message.message_id),
                    lambda: client.kick_chat_member(member.chat.id, member.new_chat_member.user.id, 3000)
            )
            future.add_done_callback(callback)
            futures[(member.chat.id, member.new_chat_member.user.id)] = future
            client.loop.call_later(
                60,
                callback
            )
