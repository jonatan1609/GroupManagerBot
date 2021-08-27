from ..filters import change_language_callback, change_language_text
from pyrogram import Client, types
from pony.orm import db_session
from ..database import Group, User
from .. import strings, config
from .start import keyboard


@Client.on_callback_query(change_language_callback)
def change_language_callback(_: Client, callback: types.CallbackQuery):
    language, _, group = callback.data.split("=")[1].partition(';')
    with db_session:
        if callback.data[4] == "s":
            group = Group.get(id=int(group))
            if group and group.default_language != language:
                group.default_language = language
            callback.answer(getattr(strings, language).language_has_been_changed)
            callback.message.edit_text(getattr(strings, language).welcome_to_panel)
        else:
            user = User[callback.from_user.id]
            if user.language != language:
                user.language = language
            callback.answer(getattr(strings, language).language_has_been_changed)
            callback.message.edit(getattr(strings, language).welcome_to_the_bot.format(config.bot.name))


@Client.on_message(change_language_text)
def change_language_text(_: Client, message: types.Message):
    message.reply(
        strings.welcome_to_bot_new.format(message.from_user.first_name, config.bot.name),
        reply_markup=keyboard
    )
