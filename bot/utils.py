async def fetch_admins(client, message):
    administrators = [
        (x.user.id, x.user.first_name, x.user.last_name, x.status)
        async for x in client.iter_chat_members(
            message.chat.id,
            filter="administrators"
        )
    ]
    creator = next((x for x in administrators if x[-1] == "creator"), 0)
    if creator:
        administrators.remove(creator)

    return creator, administrators
