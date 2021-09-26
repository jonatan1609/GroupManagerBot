from pyrogram import Client, types
from ..filters import group
from asyncio import Future
from .. import futures, remove_future, strings, config, cache, banned_permissions
from random import sample
from pony.orm import db_session
from ..database import Group, User
from ..utils import fetch_admins, is_member
from loguru import logger


@Client.on_chat_member_updated(group)
async def member_has_joined(client: Client, member: types.ChatMemberUpdated):
    if is_member(member):
        if member.new_chat_member.user.is_self:
            logger.info(f"Bot was added to group {member.chat.id} [{member.chat.title!r}]")
            with db_session:
                creator, administrators = await fetch_admins(client, member.chat.id)
                user = User.get(id=creator[0])
                if not user:
                    logger.debug(f"User {creator[0]} not found,"
                                 f" adding to database")
                    user = User(
                        id=creator[0] or -1,
                        first_name=creator[1] or "Deleted account",
                        last_name=creator[2] or ""
                    )
                if not Group.get(id=member.chat.id):
                    administrators = [
                        User.get(id=x[0]) or User(id=x[0], first_name=x[1] or "Deleted Account", last_name=x[2] or "")
                        for x in administrators
                    ]
                    logger.debug(f"Group {member.chat.id} not found,"
                                 f" adding to database")
                    Group(
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
            group = Group.get(id=member.chat.id)
            if not group:
                logger.error(f"Group {member.chat.id} is not in database")
                await client.send_message(
                    member.chat.id,
                    strings.readd_group
                )
                return await member.chat.leave()
        logger.info(f"Restricting user {member.new_chat_member.user.id}")
        await member.chat.restrict_member(
            member.new_chat_member.user.id,
            banned_permissions
        )
        if message := await client.send_message(
            member.chat.id, getattr(
                    strings, group.default_language
                ).welcome_to_the_group.format(
                f"[{member.new_chat_member.user.first_name}]"
                f"(tg://user?id={member.new_chat_member.user.id})",
                group.time_to_ban,
            ), reply_markup=types.InlineKeyboardMarkup([
                    *sample([
                        [types.InlineKeyboardButton(
                            getattr(
                                strings, group.default_language
                            ).i_am_a_bot,
                            callback_data="bot"
                        )],
                        [types.InlineKeyboardButton(
                                getattr(
                                    strings, group.default_language
                                ).i_am_a_human,
                                callback_data="human"
                        )]
                    ], 2)
                ])
        ):
            future = Future()
            callback = lambda *_: remove_future(
                future,
                (
                    member.chat.id,
                    member.new_chat_member.user.id,
                    message.message_id
                ),
                lambda: client.kick_chat_member(
                    member.chat.id,
                    member.new_chat_member.user.id
                )
            )
            future.add_done_callback(callback)
            futures[
                (
                    member.chat.id,
                    member.new_chat_member.user.id,
                    message.message_id
                )
            ] = future
            client.loop.call_later(
                60,
                callback
            )
            if not cache["permissions"].get(member.chat.id):
                cache["permissions"][member.chat.id] = member.chat.permissions
