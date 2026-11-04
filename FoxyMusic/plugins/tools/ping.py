# ─────「 𝐅ᴏxʏ 」─────
#    Official Project Source
# ────────────────────────
# Copyright (C) 2021-2022 by Yuki77394@Github, < https://github.com/yuki77394 >.
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Yuki77394/FoxyMusic/blob/master/LICENSE >
# All rights reserved.

from FoxyMusic.core.client_context import get_client
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from FoxyMusic import app
from FoxyMusic.core.call import Alone
from FoxyMusic.utils import bot_sys_stats
from FoxyMusic.utils.decorators.language import language
from FoxyMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"].format(get_client().mention),
    )
    pytgping = await Alone.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, get_client().mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
