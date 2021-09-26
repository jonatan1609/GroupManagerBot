from pyrogram import Client, errors
from loguru import logger
from ..filters import service


@Client.on_message(service)
async def delete_service_messages(_, message):
    try:
        await message.delete()
        logger.info("Deleting a service message")
    except errors.RPCError:
        logger.error("Could not delete message")
