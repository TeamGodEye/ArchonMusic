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
        await get_client().send_document(
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
    if await is_on_off(2):
        logger_text = f"""<blockquote>
<b>{get_client().mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> {message.chat.title}
<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.chat.username}

<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>
<b>ɴᴀᴍᴇ :</b> {message.from_user.mention}
<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}

<b>ǫᴜᴇʀʏ :</b> {message.text.split(None, 1)[1]}
<b>sᴛʀᴇᴀᴍᴛʏᴘᴇ :</b> {streamtype}</blockquote>"""
        if message.chat.id != LOGGER_ID:
            try:
                await get_client().send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return
