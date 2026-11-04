# ─────「 𝐀ʀᴄʜᴏɴ 」─────
# Shared play logging for the main bot and registered clones.

import html
import os

from pyrogram.enums import ParseMode

from FoxyMusic import app
from FoxyMusic.core.client_context import get_client
from FoxyMusic.utils.database import is_on_off
from config import LOGGER_ID


def _safe(value):
    return html.escape(str(value if value not in (None, "") else "Unknown"), quote=False)


async def send_large_error(trace, caption, filename):
    """Send error reports through the main bot, so clones needn't join LOGGER_ID."""
    with open(filename, "w", encoding="utf-8") as f:
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
    finally:
        try:
            os.remove(filename)
        except Exception:
            pass


async def _chat_details(message, client):
    owner = "Unknown"
    members = "Unknown"
    chat = getattr(message, "chat", None)
    if not chat or not getattr(chat, "title", None):
        return owner, members
    try:
        async for member in client.get_chat_members(chat.id, filter="administrators"):
            status = getattr(getattr(member, "status", None), "value", str(getattr(member, "status", ""))).lower()
            if status in ("owner", "creator"):
                user = getattr(member, "user", None)
                if user:
                    owner = getattr(user, "mention", None) or getattr(user, "first_name", "Unknown")
                break
    except Exception:
        pass
    try:
        members = str(await client.get_chat_members_count(chat.id))
    except Exception:
        pass
    return owner, members


async def play_logs(message, streamtype):
    if not await is_on_off(2):
        return

    source_client = get_client()
    # Determine the bot identity by Telegram user ID, not by a display label.
    # The main bot must show PLAY LOG; only different bot identities show CLONE BOT LOG.
    try:
        source_me = await source_client.get_me()
    except Exception:
        source_me = None
    try:
        main_me = await app.get_me()
    except Exception:
        main_me = getattr(app, "me", None)

    source_id = getattr(source_me, "id", None)
    main_id = getattr(main_me, "id", None)
    is_clone = bool(source_id and main_id and source_id != main_id)
    username = getattr(source_me, "username", None) or getattr(source_client, "username", None)
    bot_label = f"@{_safe(username)}" if username else _safe(getattr(source_client, "mention", "Music bot"))

    chat = getattr(message, "chat", None)
    user = getattr(message, "from_user", None)
    raw_text = getattr(message, "text", None) or getattr(message, "caption", None) or ""
    parts = raw_text.split(maxsplit=1)
    query = parts[1] if len(parts) > 1 else "Unknown"
    chat_title = getattr(chat, "title", None) or getattr(chat, "first_name", None) or "Private chat"
    chat_id = getattr(chat, "id", "Unknown")
    requester = getattr(user, "mention", None) or getattr(user, "first_name", None) or "Unknown"
    requester_id = getattr(user, "id", "Unknown")
    requester_username = getattr(user, "username", None)

    owner, members = await _chat_details(message, source_client)
    if is_clone:
        heading = f"<b>🤖 CLONE BOT LOG:</b> {bot_label}"
    else:
        heading = f"<b>✦ PLAY LOG</b>\n<b>BOT:</b> {bot_label}"

    log_text = (
        f"<blockquote>{heading}\n\n"
        f"<b>• REQUEST BY:</b> {requester}\n"
        f"<b>• USER ID:</b> <code>{_safe(requester_id)}</code>\n"
        f"<b>• USERNAME:</b> @{_safe(requester_username)}\n"
        f"<b>• QUERY:</b> {_safe(query)}\n"
        f"<b>• CHAT:</b> {_safe(chat_title)} [<code>{_safe(chat_id)}</code>]\n"
        f"<b>• OWNER:</b> {_safe(owner)}\n"
        f"<b>• MEMBERS:</b> {_safe(members)}\n"
        f"<b>• STREAM TYPE:</b> {_safe(streamtype)}</blockquote>"
    )
    try:
        # The main bot posts both main and clone logs into the shared logger group.
        await app.send_message(
            chat_id=LOGGER_ID,
            text=log_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except Exception:
        # Logging must never interrupt playback.
        pass
