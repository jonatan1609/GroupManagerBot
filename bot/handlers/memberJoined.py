from pyrogram import Client, types
from ..filters import group
from asyncio import Future
from .. import futures, remove_future, strings, config
from random import sample
from pony.orm import db_session
from ..database import Group, User


@Client.on_chat_member_updated(group)
async def member_has_joined(client: Client, member: types.ChatMemberUpdated):
    if (
            member.new_chat_member
            and member.new_chat_member.status not in {"kicked", "left", "restricted"}
            and not member.old_chat_member
    ):
        if member.new_chat_member.user.is_self:
            administrators = []
            with db_session:
                administrators = [
                    (x.user.id, x.user.first_name, x.user.last_name, x.status)
                    async for x in client.iter_chat_members(
                        member.chat.id,
                        filter="administrators"
                    )
                ]
                creator = next((x for x in administrators if x[-1] == "creator"), 0)
                if creator:
                    administrators.remove(creator)
                user = User.get(id=creator[0])
                if not user:
                    user = User(
                        id=creator[0] or -1,
                        first_name=creator[1] or "Deleted account",
                        last_name=creator[2] or ""
                    )
                group = Group.get(id=member.chat.id)
                if not group:
                    administrators = [User(id=x[0], first_name=x[1], last_name=x[2] or "") for x in administrators]
                    group = Group(
                        id=member.chat.id,
                        owner=user,
                        administrators=administrators
                    )
            return await client.send_message(
                member.chat.id,
                strings.bot_was_added,
                reply_markup=types.InlineKeyboardMarkup([
                    [types.InlineKeyboardButton(
                        strings.button_config,
                        url=f"t.me/{config.bot.username}?start={member.chat.id}"
                    )]
                ])
            )
        with db_session:
            group = Group[member.chat.id]
        if message := await client.send_message(
            member.chat.id, getattr(strings, group.default_language).welcome_to_the_group.format(
                f"[{member.new_chat_member.user.first_name}](tg://user?id={member.new_chat_member.user.id})",
                group.time_to_ban,
            ), reply_markup=types.InlineKeyboardMarkup([
                    *sample([
                        [types.InlineKeyboardButton(getattr(strings, group.default_language).i_am_a_bot, callback_data="bot")],
                        [types.InlineKeyboardButton(getattr(strings, group.default_language).i_am_a_human, callback_data="human")]
                    ], 2)
                ])
        ):
            future = Future()
            callback = lambda *_: remove_future(
                future,
                (member.chat.id, member.new_chat_member.user.id, message.message_id),
                lambda: client.kick_chat_member(member.chat.id, member.new_chat_member.user.id)
            )
            future.add_done_callback(callback)
            futures[(member.chat.id, member.new_chat_member.user.id, message.message_id)] = future
            client.loop.call_later(
                60,
                callback
            )
