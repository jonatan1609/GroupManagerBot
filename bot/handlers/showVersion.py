from ..filters import version
from pyrogram import Client, types
from .. import __version__


@Client.on_message(version)
def show_version(_: Client, message: types.Message):
    message.reply(str(__version__))
