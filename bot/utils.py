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
    return (await client.get_chat(chat_id)).title


def format_admins(creator: str, admins: list, wrap: callable = str, key=lambda x: x):
    upper = "╔"
    middle = "╟"
    bottom = "╙"
    line = "─"
    creator_line = "═"
    lines = []
    if admins:
        lines.append(upper + creator_line * len(max(admins, key=key)[1] or 4) + wrap(creator))
        lines.extend([middle + line + wrap(admin) for admin in admins[:-1]])
        lines.append(bottom + line + wrap(admins[-1]))
    else:
        lines.insert(1, creator_line + wrap(creator))
    return "\n".join(lines)
