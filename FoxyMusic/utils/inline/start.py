# ─────「 𝐅ᴏxʏ 」─────
#    Official Project Source
# ────────────────────────

from FoxyMusic.core.client_context import get_client
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

import config
from FoxyMusic import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{get_client().username}?startgroup=true",
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
                url=f"https://t.me/{get_client().username}?startgroup=true",
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
                text="ᴅєᴠєʟᴏᴘєʀ",
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
