# ─────「 𝐅ᴏxʏ 」─────
#    Official Project Source
# ────────────────────────
# Copyright (C) 2021-2022 by Yuki77394@Github, < https://github.com/yuki77394 >.
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Yuki77394/FoxyMusic/blob/master/LICENSE >
# All rights reserved.

from FoxyMusic.core.client_context import get_client
from FoxyMusic import app
from FoxyMusic.utils.database import get_cmode


async def get_channeplayCB(_, command, CallbackQuery):
    if command == "c":
        chat_id = await get_cmode(CallbackQuery.message.chat.id)
        if chat_id is None:
            try:
                return await CallbackQuery.answer(_["setting_7"], show_alert=True)
            except:
                return
        try:
            channel = (await get_client().get_chat(chat_id)).title
        except:
            try:
                return await CallbackQuery.answer(_["cplay_4"], show_alert=True)
            except:
                return
    else:
        chat_id = CallbackQuery.message.chat.id
        channel = None
    return chat_id, channel
