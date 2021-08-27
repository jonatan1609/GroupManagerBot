from ..filters import version
from pyrogram import Client, types
from .. import __version__


@Client.on_message(version)
async def show_version(_: Client, message: types.Message):
    await message.reply(__version__)
