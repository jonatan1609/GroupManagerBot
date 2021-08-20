from pyrogram import filters

group = filters.group
private = filters.private
start = filters.command("start")
start_config = start & private & filters.create(lambda _, __, m: len(m.command) > 1)
human = filters.regex("^human$")
bot = filters.regex("^bot$")
change_language = filters.regex("^lang")
