from ..filters import start_config
from .. import strings
from ..languages_enum import LanguagesEnum
from ..database import Group
from pyrogram import Client, types, errors
from pony.orm import db_session
from loguru import logger


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
        group_db_obj = Group.get(id=group)
        if not group_db_obj:
            logger.error(f"Group {group} is not in database")
            await message.reply(strings.readd_group, quote=False)
            try:
                await client.send_message(group, strings.readd_group)
            except errors.RPCError as e:
                logger.error(e.MESSAGE)
            try:
                await client.leave_chat(group)
            except errors.RPCError as e:
                logger.error(e.MESSAGE)
            return
        is_allowed_admin = message.from_user.id in [x.id for x in (*group_db_obj.administrators, group_db_obj.owner)]
    if is_allowed_admin:
        await client.send_message(
            message.chat.id,
            strings.choose_language.format(message.from_user.first_name),
            reply_markup=types.InlineKeyboardMarkup(split(LanguagesEnum.map(), group))
        )
