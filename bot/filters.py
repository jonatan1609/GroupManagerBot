from pyrogram import filters

group = filters.group
private = filters.private
start = filters.command("start")
start_config = start & private & filters.create(lambda _, __, m: len(m.command) > 1)
human = filters.regex("^human$")
bot = filters.regex("^bot$")
change_language_callback = filters.regex("^lang")
change_language_text = private & filters.command("language")
refresh_admins_list = filters.command("admins")
version = filters.command('version')
