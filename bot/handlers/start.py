from ..filters import start, private
from ..database import User
from ..languages_enum import LanguagesEnum
from .. import strings, config
from .configBotInPM import split
from pony.orm import db_session
from pyrogram import Client, types

keyboard = types.InlineKeyboardMarkup(split(LanguagesEnum.map(), -1))


@Client.on_message(private & start)
async def start(_: Client, message: types.Message):
    with db_session:
        if not User.get(id=message.from_user.id):
            User(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name or "",
            )
            await message.reply(
                strings.welcome_to_bot_new.format(message.from_user.first_name, config.bot.name),
                reply_markup=keyboard
            )
        else:
            await message.reply(
                getattr(strings, User[message.from_user.id].language).welcome_to_the_bot.format(
                    config.bot.name
                )
            )
