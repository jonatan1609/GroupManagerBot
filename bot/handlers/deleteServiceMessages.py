from pyrogram import Client
from ..filters import service


@Client.on_message(service)
async def delete_service_messages(_, message):
    await message.delete()
