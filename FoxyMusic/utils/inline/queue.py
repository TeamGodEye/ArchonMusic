# ─────「 𝐅ᴏxʏ 」─────
#    Official Project Source
# ────────────────────────
# Copyright (C) 2021-2022 by Yuki77394@Github, < https://github.com/yuki77394 >.
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Yuki77394/FoxyMusic/blob/master/LICENSE >
# All rights reserved.

from typing import Union

from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[bool, int] = None,
    dur: Union[bool, int] = None,
):
    """Inline keyboard for the now-playing message footer.

    Two layouts depending on whether the duration is known:
      - DURATION == "Unknown" : [Queue] [Close]
      - DURATION known         : [Timer/Progress] / [Queue] [Close]

    Callbacks fired:
      - "GetQueued {CPLAY}|{videoid}"  → opens the queue list view
      - "GetTimer"                     → shows the playback progress bar
      - "close"                         → closes the now-playing message
    """
    not_dur = [
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=ButtonStyle.DANGER,
            ),
        ]
    ]
    dur = [
        [
            InlineKeyboardButton(
                text=_["QU_B_2"].format(played, dur),
                callback_data="GetTimer",
                style=ButtonStyle.SUCCESS,
            )
        ],
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=ButtonStyle.DANGER,
            ),
        ],
    ]
    upl = InlineKeyboardMarkup(not_dur if DURATION == "Unknown" else dur)
    return upl


def queue_back_markup(_, CPLAY):
    """Back + Close row shown in the queue view after clicking GetTimer.

    Callbacks fired:
      - "queue_back_timer {CPLAY}"  → returns to the timer/progress view
      - "close"                     → closes the message
    """
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"queue_back_timer {CPLAY}",
                    style=ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=ButtonStyle.DANGER,
                ),
            ]
        ]
    )
    return upl


def aq_markup(_, chat_id):
    """Close button for the "Added to Queue" notification.

    Accepts (_, chat_id) to match the call signature used in
    FoxyMusic/utils/stream/stream.py (the chat_id argument is accepted
    for signature compatibility but is not currently used in the layout).

    Callbacks fired:
      - "close"  → dismisses the added-to-queue notification
    """
    buttons = [
        [InlineKeyboardButton(
            text="⌯ ᴄʟᴏsє ⌯",
            callback_data="close",
            style=ButtonStyle.DANGER,
        )],
    ]
    return buttons
