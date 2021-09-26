from . import client, strings
from pyrogram import types
from loguru import logger


async def main():
    commands = {
        language: [
            types.BotCommand(x.split(' - ')[0].lstrip('/'), x.split(' - ')[1])
            for x in getattr(strings, language).available_commands
        ] for language in ("Hebrew", "English")
    }
    async with client:
        languages = commands.keys()
        for language, commands in commands.items():
            await client.set_bot_commands(
                commands,
                scope=types.BotCommandScopeAllPrivateChats(),
                language_code=language[:2].lower()
            )
    logger.info("Bot commands have been set successfully ({})".format(
        ", ".join(languages)
    ))
