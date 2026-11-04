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
    return html.escape(str(value if value not in (None, "") else "Unknown"))


async def send_large_error(trace, caption, filename):
    """Send error reports through the main bot so clones needn't join LOGGER_ID."""
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
    try:
        chat = await client.get_chat(message.chat.id)
        if getattr(chat, "title", None):
            # Pyrogram exposes owner identity through chat_member status in a
            # member list; avoid scanning the entire group for performance.
            async for member in client.get_chat_members(message.chat.id, filter="administrators"):
                if getattr(getattr(member, "status", None), "value", str(getattr(member, "status", ""))).lower() in ("owner", "creator"):
                    user = getattr(member, "user", None)
                    if user:
                        owner = getattr(user, "mention", None) or getattr(user, "first_name", "Unknown")
                    break
        try:
            members = str(await client.get_chat_members_count(message.chat.id))
        except Exception:
            pass
    except Exception:
        pass
    return owner, members


async def play_logs(message, streamtype):
    if not await is_on_off(2):
        return

    # The handler's context client is the clone that received this play request;
    # app is always the main bot and posts the log to the shared logger group.
    source_client = get_client()
    bot_username = getattr(source_client, "username", None)
    if not bot_username:
        try:
            me = await source_client.get_me()
            bot_username = getattr(me, "username", None)
        except Exception:
            bot_username = None
    bot_label = f"@{_safe(bot_username)}" if bot_username else _safe(getattr(source_client, "mention", "Music bot"))

    chat = getattr(message, "chat", None)
    user = getattr(message, "from_user", None)
    text = getattr(message, "text", None) or getattr(message, "caption", None) or ""
    parts = text.split(maxsplit=1)
    query = parts[1] if len(parts) > 1 else "Unknown"
    chat_title = getattr(chat, "title", None) or getattr(chat, "first_name", None) or "Private chat"
    chat_id = getattr(chat, "id", "Unknown")
    chat_username = getattr(chat, "username", None)
    requester = getattr(user, "mention", None) or getattr(user, "first_name", None) or "Unknown"
    requester_id = getattr(user, "id", "Unknown")
    requester_username = getattr(user, "username", None)

    owner, members = await _chat_details(message, source_client) if chat and getattr(chat, "title", None) else ("Unknown", "Unknown")
    log_text = (
        f"<blockquote><b>🤖 CLONE BOT LOG:</b> {bot_label}\n\n"
        f"<b>• REQUEST BY:</b> {requester}\n"
        f"<b>• USER ID:</b> <code>{_safe(requester_id)}</code>\n"
        f"<b>• USERNAME:</b> @{_safe(requester_username)}\n"
        f"<b>• QUERY:</b> {_safe(query)}\n"
        f"<b>• CHAT:</b> {_safe(chat_title)} [<code>{_safe(chat_id)}</code>]\n"
        f"<b>• OWNER:</b> {owner}\n"
        f"<b>• MEMBERS:</b> {_safe(members)}\n"
        f"<b>• STREAM TYPE:</b> {_safe(streamtype)}</blockquote>"
    )
    try:
        # Always send with the main bot, so clone bots do not need LOGGER_ID access.
        await app.send_message(
            chat_id=LOGGER_ID,
            text=log_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except Exception:
        # Logging must never interrupt playback.
        pass
