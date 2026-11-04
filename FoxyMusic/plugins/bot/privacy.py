# ─────「 𝐅ᴏxʏ 」─────
#    Official Project Source
# ────────────────────────

from pyrogram import filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from FoxyMusic import app
from FoxyMusic.utils.decorators.language import language
from config import BANNED_USERS, PRIVACY_LINK

@app.on_message(filters.command("privacy") & ~BANNED_USERS)
@language
async def privacy_policy(client, message: Message, _):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["PRIVACY_BUTTON"],
                url=config.PRIVACY_LINK,
                style=ButtonStyle.PRIMARY,
            ),
        ],
    ]
    await message.reply_text(
        _["privacy_1"],
        reply_markup=InlineKeyboardMarkup(buttons),
    )
