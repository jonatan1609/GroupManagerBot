from ..filters import change_language
from pyrogram import Client, types
from pony.orm import db_session
from ..database import Group
from .. import strings


@Client.on_callback_query(change_language)
def change_language(_: Client, callback: types.CallbackQuery):
    language, group = callback.data[5:].split(';')
    with db_session:
        group = Group.get(id=int(group))
        if group and group.default_language != language:
            group.default_language = language
    callback.answer(getattr(strings, group.default_language).language_has_been_changed)
