from ..filters import start_config
from .. import strings
from ..languages_enum import LanguagesEnum
from ..database import Group
from pyrogram import Client, types
from pony.orm import db_session


def split(array: list, group: int) -> list:
    s = "s" if group != -1 else ""
    return [
        [types.InlineKeyboardButton(x, f'lang{s}={x};{group}')
         for x in array[x: x + 2]] for x in range(0, len(array), 2)
    ]


@Client.on_message(start_config)
async def start_config(client: Client, message: types.Message):
    group = int(message.command[-1])
    with db_session:
        group_db_obj = Group[group]
        allowed_admin = message.from_user.id in [x.id for x in (*group_db_obj.administrators, group_db_obj.owner)]
    if allowed_admin:
        await client.send_message(
            message.chat.id,
            strings.choose_language.format(message.from_user.first_name),
            reply_markup=types.InlineKeyboardMarkup(split(LanguagesEnum.map(), group))
        )
