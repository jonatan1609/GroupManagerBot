from pyrogram.types import ChatMemberUpdated
from pyrogram import errors


async def fetch_admins(client, chat_id):
    administrators = [
        (x.user.id, x.user.first_name, x.user.last_name, x.status)
        async for x in client.iter_chat_members(
            chat_id,
            filter="administrators"
        )
    ]
    creator = next((x for x in administrators if x[-1] == "creator"), 0)
    if creator:
        administrators.remove(creator)
    return creator, administrators


async def fetch_group_name(client, chat_id):
    try:
        return (await client.get_chat(chat_id)).title
    except errors.RPCError:
        return -1


def format_admins(
        creator: tuple,
        admins: list,
        wrap: callable = str,
        key=lambda x: x
):
    upper = "╔"
    middle = "╟"
    bottom = "╙"
    line = "─"
    creator_line = "═"
    lines = []
    if admins:
        lines.append(upper + creator_line * (
                len(max(admins, key=key)[1] or 4) - len(creator)
        ) + wrap(creator))
        lines.extend([middle + line + wrap(admin) for admin in admins[:-1]])
        lines.append(bottom + line + wrap(admins[-1]))
    else:
        lines.insert(1, creator_line + wrap(creator))
    return "\n".join(lines)


def is_member(update: ChatMemberUpdated) -> bool:
    new = False
    if update.old_chat_member and update.new_chat_member:
        if update.old_chat_member.status == "restricted":
            if not update.old_chat_member.is_member \
                    and update.new_chat_member.is_member:
                new = True
    elif update.new_chat_member and not update.old_chat_member:
        if update.new_chat_member.status in {"restricted", "member"}:
            new = True
    return new


def shorten(obj) -> str:
    as_str = str(obj)
    if len(as_str) > 10:
        as_str = as_str[:5] + " ... " + as_str[-2:]

    return as_str
