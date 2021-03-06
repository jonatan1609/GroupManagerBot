from ..filters import change_language_callback, change_language_text
from pyrogram import Client, types
from pony.orm import db_session
from ..database import Group, User
from .. import strings, config
from .start import keyboard
from loguru import logger


@Client.on_callback_query(change_language_callback)
async def change_language_callback(_: Client, callback: types.CallbackQuery):
    language, _, group = callback.data.split("=")[1].partition(';')
    with db_session:
        if callback.data[4] == "s":
            db_group = Group.get(id=int(group))
            if db_group and db_group.default_language != language:
                db_group.default_language = language
            elif not db_group:
                logger.debug(f"Group {group} not found")
                return await callback.message.edit(
                    getattr(strings, language).group_not_found
                )
            await callback.answer(getattr(strings, language).language_has_been_changed)
            await callback.message.edit_text(getattr(strings, language).welcome_to_panel)
        else:
            user = User.get(id=callback.from_user.id)
            if not user:
                logger.debug(f"User {callback.from_user.id} not found,"
                             f" adding to database")
                user = User(
                    id=callback.from_user.id,
                    first_name=callback.from_user.first_name,
                    last_name=callback.from_user.last_name or "",
                    language=language
                )
            if user.language != language:
                user.language = language
            await callback.answer(getattr(strings, language).language_has_been_changed)
            await callback.message.edit(getattr(strings, language).welcome_to_the_bot.format(config.bot.name))


@Client.on_message(change_language_text)
async def change_language_text(_: Client, message: types.Message):
    await message.reply(
        strings.welcome_to_bot_new.format(message.from_user.first_name, config.bot.name),
        reply_markup=keyboard
    )
