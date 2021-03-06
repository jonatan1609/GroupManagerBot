from ..database import User, Group
from pony.orm import db_session
from pyrogram import Client, types, errors
from ..utils import fetch_admins, fetch_group_name, format_admins
from .. import cache, strings
from ..filters import (
    show_admins_list,
    select_group__show_admins,
    refresh_admins_list
)
from loguru import logger


def split(array: list, prefix: str):
    return [
        [
            types.InlineKeyboardButton(
                cache["names"].get(chat, "<unknown>"),
                f"{prefix}={chat}"
            ) for chat in array[x: x + 2]
        ]
        for x in range(0, len(array), 2)
    ]


@Client.on_message(show_admins_list)
async def show_admins_list(client: Client, message: types.Message):
    groups = []
    with db_session:
        user = User.get(id=message.from_user.id)
        if not user:
            logger.debug(f"User {message.from_user.id} not found,"
                         f" adding to database")
            return await message.reply(
                getattr(strings, user.language).no_groups
            )
        groups.extend([
            group.id for group in (
                    [group for group in user.admin_in_groups] +
                    [group for group in user.owning_groups]
            )
        ])
        not_found = []
        for group in groups:
            if group not in cache["names"]:
                logger.info(f"fetching group name for {group}")
                name = await fetch_group_name(client, group)
                if name != -1:
                    cache["names"].insert(
                        group, name
                    )
                else:
                    not_found.append(group)
                    logger.error(f"Could not find group {group}")
            if group not in cache["admins"] and group not in not_found:
                logger.info(f"Fetching admins list for {group}")
                cache["admins"].insert(group, await fetch_admins(client, group))
        if not_found:
            m = getattr(strings, user.language).chats_not_found.format("\n".join(map(str, not_found)))
            for g in not_found:
                groups.remove(g)
                with db_session:
                    db_g = Group.get(id=g)
                    if db_g:
                        db_g.delete()
            await message.reply(m, quote=False)
        if groups:
            await message.reply(
                getattr(strings, user.language).choose_group,
                reply_markup=types.InlineKeyboardMarkup(split(groups, "adm"))
            )
        else:
            await message.reply(
                getattr(strings, user.language).no_groups
            )


@Client.on_callback_query(select_group__show_admins)
async def show_admins(client: Client, callback: types.CallbackQuery):
    _, _, group = callback.data.partition("=")
    group = int(group)
    if group not in cache["admins"]:
        logger.info(f"Fetching admins list for {group}")
        cache["admins"].insert(group, await fetch_admins(client, group))
    creator, admins = cache["admins"][group]
    with db_session:
        user = User.get(id=callback.from_user.id)
        if not user:
            return logger.debug(f"User {callback.from_user.id} not found,"
                                f" adding to database")
    admins = format_admins(
        creator=creator,
        admins=admins,
        wrap=lambda admin: f"\u200e[{admin[1]}]"
                           f"(tg://user?id={admin[0]})"
                           if admin[1] else "Deleted Account",
        key=lambda admin: len(admin[1] or ""),
    )
    await callback.message.edit(
        getattr(strings, user.language).your_admins_list + admins,
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton(
                getattr(strings, user.language).refresh_admins,
                f"refadm={group}"
            )]
        ])
    )


@Client.on_callback_query(refresh_admins_list)
async def refresh_admins_list(client: Client, callback: types.CallbackQuery):
    _, _, group = callback.data.partition('=')
    group = int(group)
    logger.info(f"Fetching admins list for {group}")
    cache["admins"].insert(group, await fetch_admins(client, group))
    try:
        await show_admins(client, callback)
    except errors.MessageNotModified:
        pass
        # This means there is no new admin
