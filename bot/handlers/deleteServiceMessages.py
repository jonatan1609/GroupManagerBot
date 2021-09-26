from pyrogram import Client, errors
from loguru import logger
from ..filters import service


@Client.on_message(service)
async def delete_service_messages(_, message):
    try:
        logger.info("Deleting a service message")
        await message.delete()
    except errors.RPCError:
        logger.error("Could not delete message")
