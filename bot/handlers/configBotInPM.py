from ..filters import start_config
from .. import strings
from ..languages_enum import LanguagesEnum
from pyrogram import Client, types


def split(array: list, group: int) -> list:
    return [[types.InlineKeyboardButton(x, f'lang={x};{group}') for x in array[x: x + 2]] for x in range(0, len(array), 2)]


@Client.on_message(start_config)
async def start_config(client: Client, message: types.Message):
    group = int(message.command[-1])
    await client.send_message(
        message.chat.id,
        strings.choose_language.format(message.from_user.first_name),
        reply_markup=types.InlineKeyboardMarkup(split(LanguagesEnum.map(), group))
    )
