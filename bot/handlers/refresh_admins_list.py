from ..database import Group, User
from pony.orm import db_session
from pyrogram import Client, types
from ..filters import refresh_admins_list
from ..utils import fetch_admins


@Client.on_message(refresh_admins_list)
async def refresh_admins_list(client: Client, message: types.Message):
    with db_session:
        groups = User.get(id=message.from_user.id)
        groups = ([group for group in groups.admin_in_groups] + [group for group in groups.owning_groups])
"""
creator, administrators = await fetch_admins(client, message.chat.id)
    with db_session:
        creator = User.get(id=creator[0])
        if not creator:
            creator = User(
                id=creator[0] or -1,
                first_name=creator[1] or "Deleted account",
                last_name=creator[2] or ""
            )
        administrators = [User(id=x[0], first_name=x[1], last_name=x[2] or "") for x in administrators]
        
    return types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton()]
    ])
"""