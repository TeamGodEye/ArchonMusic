#
# Copyright (C) 2021-2022 by Yuki77394@Github, < https://github.com/yuki77394 >.
#
# This file is part of < https://github.com/Yuki77394/FoxyMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Yuki77394/FoxyMusic/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

import config
from FoxyMusic import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id=6100125944381444896,
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],
                url=config.SUPPORT_CHAT,
                style=ButtonStyle.SUCCESS,
            ),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id=5203951816588430946,
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                callback_data="settings_back_helper",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id=5422869288962784257,
            ),
        ],
        [
            InlineKeyboardButton(
                text="Tʜᴇ Aʀᴄʜᴏɴ",
                user_id=config.OWNER_ID,
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id=5424632072390078052,
            ),
            InlineKeyboardButton(
                text="⌯ Nᴇᴛᴡᴏʀᴋ ⌯",
                url="https://t.me/FoxryHQ",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id=5422484648871626179,
            ),
        ],
    ]

    return buttons
