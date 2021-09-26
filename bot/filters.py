from pyrogram import filters

group = filters.group
private = filters.private
start = filters.command("start")
start_config = start & private & filters.create(lambda _, __, m: len(m.command) > 1)
human = filters.regex("^human$")
bot = filters.regex("^bot$")
change_language_callback = filters.regex("^lang")
change_language_text = private & filters.command("language")
version = filters.command('version')
show_admins_list = private & filters.command('admins')
refresh_admins_list = filters.regex('^refadm')
select_group__show_admins = filters.regex("^adm=")
service = filters.group & filters.service
