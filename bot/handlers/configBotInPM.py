from ..filters import start_config
from pyrogram import Client, types


@Client.on_message(start_config)
async def start_config(client: Client, message: types.Message):
    group = int(message.command[-1])
    print([x.status async for x in client.iter_chat_members(group, filter="administrators")])

