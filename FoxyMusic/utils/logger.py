# ─────「 𝐅ᴏxʏ 」─────
#    Official Project Source
# ────────────────────────
# Copyright (C) 2021-2022 by Yuki77394@Github, < https://github.com/yuki77394 >.
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Yuki77394/FoxyMusic/blob/master/LICENSE >
# All rights reserved.

from FoxyMusic.core.client_context import get_client
import os

from pyrogram.enums import ParseMode

from FoxyMusic import app
from FoxyMusic.utils.database import is_on_off
from config import LOGGER_ID


async def send_large_error(trace, caption, filename):
    with open(filename, "w") as f:
        f.write(trace)
    try:
        await app.send_document(
            chat_id=LOGGER_ID,
            document=filename,
            caption=caption,
            parse_mode=ParseMode.HTML,
        )
    except Exception:
        pass
    try:
        os.remove(filename)
    except Exception:
        pass


async def play_logs(message, streamtype):
    """Send main and clone playback logs through the primary bot to LOGGER_ID."""
    if not await is_on_off(2):
        return

    active_client = get_client()
    main_id = getattr(app, "id", None)
    active_id = getattr(active_client, "id", None)
    is_clone = bool(active_id and main_id and active_id != main_id)
    bot_username = getattr(active_client, "username", None) or "Unknown"
    heading = (
        f"🤖 <b>CLONE BOT LOG:</b>\n@{bot_username}"
        if is_clone
        else "✦ <b>PLAY LOG</b>"
    )

    chat = getattr(message, "chat", None)
    user = getattr(message, "from_user", None)
    if chat is None or user is None:
        return

    query = ""
    text = getattr(message, "text", None) or getattr(message, "caption", None) or ""
    parts = text.split(None, 1)
    if len(parts) > 1:
        query = parts[1]
    if not query:
        query = "Unknown"

    chat_name = getattr(chat, "title", None) or getattr(chat, "first_name", None) or "Unknown"
    chat_username = getattr(chat, "username", None)
    user_username = getattr(user, "username", None)
    user_name = getattr(user, "mention", None) or getattr(user, "first_name", None) or "Unknown"
    logger_text = f"""<blockquote>
{heading}

<b>REQUEST BY :</b> {user_name}
<b>USER ID:</b> <code>{user.id}</code>
<b>USERNAME:</b> @{user_username or 'Unknown'}
<b>QUERY :</b> {query}
<b>CHAT :</b> {chat_name}{f' (@{chat_username})' if chat_username else ''} [<code>{chat.id}</code>]
<b>OWNER:</b> Unknown
<b>MEMBERS:</b> Unknown
<b>STREAM TYPE:</b> {streamtype}</blockquote>"""
    try:
        # Always use the primary bot to deliver to the configured logger group.
        await app.send_message(
            chat_id=LOGGER_ID,
            text=logger_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except Exception:
        # Logging must never break playback if the logger group is unavailable.
        pass
