# ─────「 𝐅ᴏxʏ 」─────
#    Official Project Source
# ────────────────────────

from FoxyMusic.core.bot import Alone
from FoxyMusic.core.dir import dirr
from FoxyMusic.core.userbot import Userbot
from FoxyMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
dbb()
heroku()

app = Alone()
from FoxyMusic.core.client_context import set_main_client
set_main_client(app)
userbot = Userbot()


from .platforms import (Apple, Carbon, Resso, Soundcloud, Spotify, Telegram,
                        Youtube)

Apple = Apple.AppleAPI()
Carbon = Carbon.CarbonAPI()
SoundCloud = Soundcloud.SoundAPI()
Spotify = Spotify.SpotifyAPI()
Resso = Resso.RessoAPI()
Telegram = Telegram.TeleAPI()
YouTube = Youtube.YouTubeAPI()
