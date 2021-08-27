from ..database import User
from pony.orm import db_session
from pyrogram import Client, types, errors
from ..utils import fetch_admins, fetch_group_name, format_admins
from .. import cache, strings
from ..filters import show_admins_list, select_group__show_admins, refresh_admins_list


def split(array: list, prefix: str):
    return [
        [
            types.InlineKeyboardButton(
                cache["names"].get(chat, "<unknown>"),
                f"{prefix}={chat}"
            ) for chat in array[x: x + 2]]
        for x in range(0, len(array), 2)
    ]


@Client.on_message(show_admins_list)
async def show_admins_list(client: Client, message: types.Message):
    with db_session:
        user = User.get(id=message.from_user.id)
        groups = [
            group.id for group in ([group for group in user.admin_in_groups] + [group for group in user.owning_groups])
        ]
        for group in groups:
            if group not in cache["names"]:
                cache["names"].insert(group, await fetch_group_name(client, group))
            if group not in cache["admins"]:
                cache["admins"].insert(group, await fetch_admins(client, group))

        await message.reply(
            getattr(strings, user.language).choose_group,
            reply_markup=types.InlineKeyboardMarkup(split(groups, "adm"))
        ),


@Client.on_callback_query(select_group__show_admins)
async def show_admins(client: Client, callback: types.CallbackQuery):
    _, _, group = callback.data.partition("=")
    group = int(group)
    if group not in cache["admins"]:
        cache["admins"].insert(group, await fetch_admins(client, group))
    creator, admins = cache["admins"][group]
    with db_session:
        user = User[callback.from_user.id]
    admins = format_admins(
        creator=creator,
        admins=admins,
        wrap=lambda admin: f"\u200e[{admin[1]}](tg://user?id={admin[0]})" if admin[1] else "Deleted Account",
        key=lambda admin: len(admin[1] or ""),
    )
    await callback.message.edit(
        getattr(strings, user.language).your_admins_list + admins,
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton(getattr(strings, user.language).refresh_admins, f"refadm={group}")]
        ])
    )


@Client.on_callback_query(refresh_admins_list)
async def refresh_admins_list(client: Client, callback: types.CallbackQuery):
    _, _, group = callback.data.partition('=')
    group = int(group)
    cache["admins"].insert(group, await fetch_admins(client, group))
    try:
        await show_admins(client, callback)
    except errors.MessageNotModified:
        pass
        # This means there is no new admin
