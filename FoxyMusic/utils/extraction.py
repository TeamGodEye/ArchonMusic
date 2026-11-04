# ─────「 𝐅ᴏxʏ 」─────
#    Official Project Source
# ────────────────────────
# Copyright (C) 2021-2022 by Yuki77394@Github, < https://github.com/yuki77394 >.
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Yuki77394/FoxyMusic/blob/master/LICENSE >
# All rights reserved.

from FoxyMusic.core.client_context import get_client
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message, User

from FoxyMusic import app


async def extract_user(m: Message) -> User:
    if m.reply_to_message:
        return m.reply_to_message.from_user
    msg_entities = m.entities[1] if m.text.startswith("/") else m.entities[0]
    return await get_client().get_users(
        msg_entities.user.id
        if msg_entities.type == MessageEntityType.TEXT_MENTION
        else int(m.command[1]) if m.command[1].isdecimal() else m.command[1]
    )
