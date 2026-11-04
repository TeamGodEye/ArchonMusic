<div align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:831843,50:DB2777,100:FBCFE8&height=220&section=header&text=FOXY%20MUSIC&fontSize=58&fontColor=FFFFFF&fontAlignY=38&desc=YOUR%20COMMUNITY.%20YOUR%20MUSIC.&descSize=16&descAlignY=58&animation=fadeIn" width="100%" alt="Foxy 
<br/><a href="https://heroku.com/deploy?template=https://github.com/FoxyPookie/FoxyMusic"><img src="https://img.shields.io/badge/🚀_DEPLOY_TO_HEROKU-9333EA?style=for-the-badge&logo=heroku&logoColor=white" alt="Deploy to Heroku"/></a>
  
<br/><img src="https://capsule-render.vercel.app/api?type=rect&height=2&color=0:831843,50:EC4899,100:FBCFE8" width="85%" alt="Divider"/></div>♡ 01 — About Foxy

Meet Foxy Music, your music companion for Telegram communities.

Designed around a simple idea: make listening together easier, with convenient playback controls and a smooth group music experience.

- 🎀 Music playback in Telegram voice chats
- 🎧 Convenient playback controls
- 💗 Queue and track management
- 🦊 A simple, community-focused experience

✧ 02 — Features

<div align="center">🎵 MUSIC| ⏯️ CONTROL
Voice chat playback| Pause, resume, skip & stop

🔎 DISCOVER| 📃 QUEUE
Supported music search| Manage upcoming tracks

🎧 ASSISTANT| 🗃️ CACHE
Assistant account support| Optional music caching

</div>♡ 03 — Built With

<div align="center"><a href="https://www.python.org/"><img src="https://skillicons.dev/icons?i=python" height="48" alt="Python"/></a>  
<a href="https://www.mongodb.com/"><img src="https://skillicons.dev/icons?i=mongodb" height="48" alt="MongoDB"/></a>  
<a href="https://git-scm.com/"><img src="https://skillicons.dev/icons?i=git" height="48" alt="Git"/></a>  
<a href="https://github.com/"><img src="https://skillicons.dev/icons?i=github" height="48" alt="GitHub"/></a>

<br/>Code with passion. Music with love. ♡

<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/FoxyPookie/FoxyMusic">
    <img src="https://img.shields.io/badge/💗_Deploy%20to-Heroku-FF69B4?style=for-the-badge&logo=heroku&logoColor=white" alt="Deploy to Heroku"/>
  </a>
</p>

</div>Quick Setup

1. Get your Telegram API credentials from "my.telegram.org" (https://my.telegram.org).
2. Create your bot through "@BotFather" (https://t.me/BotFather).
3. Prepare a MongoDB database.
4. Configure all required environment variables.
5. Deploy the project and verify the application logs.

Environment Configuration

Variable| Purpose
"API_ID"| Telegram API ID
"API_HASH"| Telegram API hash
"BOT_TOKEN"| Telegram bot token
"MONGO_DB_URI"| MongoDB connection URI
"OWNER_ID"| Bot owner's Telegram ID
"STRING_SESSION"| Assistant account session
"LOGGER_ID"| Telegram logging group ID

Configure any additional variables required by your repository. Never publish tokens, session strings or database credentials.

### ୨୧ my little corner

*where code meets creativity.* ✨

[![Foxry](https://img.shields.io/badge/Foxry_HQ-Updates-F4A7C0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/FoxryHQ)
[![Foxry Chat](https://img.shields.io/badge/Foxry_Chat-Support-E8A2B8?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/FoxryChat)

Questions, feedback or suggestions? We'd love to hear from you.

</div>♡ 06 — A Little Reminder

- Keep your credentials private.
- Use supported services responsibly.
- Playback availability depends on Telegram, dependencies and external music sources.
- Heroku deployment requires compatible configuration and an available deployment plan.

<div align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:FBCFE8,50:DB2777,100:831843&height=130&section=footer&text=Made%20with%20%E2%99%A1%20by%20Foxy&fontSize=23&fontColor=FFFFFF&fontAlignY=65" width="100%" alt="Foxy footer"/>𝐅ᴏxʏ Music — Beyond the Code. 🩷

<sub>Where music meets community.</sub>

</div>


## Clone system (KustMusic-style)

FoxyMusic can run user-owned bot tokens as clone clients. Clones reuse the same
music engine and in-memory per-chat queue: a queue is shared by chat ID, not
duplicated for each bot token. The clone bot still replies under its own
Telegram bot identity.

### Clone commands

- `/clone BOT_TOKEN` — register and start a bot created with `@BotFather`.
- `/clones` — list your clones (the main owner can view all registered clones).
- `/unclone BOT_TOKEN` — stop and remove a clone you own.
- `/unclone @username` — main-owner-only shortcut.
- `/resetclones` — main-owner command that restarts all saved clone clients.

Send tokens only in the main bot's private chat. If a token is accidentally
posted in a group, revoke it with `@BotFather` immediately.

### Enable cloning

1. Install the requirements, including `cryptography`.
2. Generate a Fernet encryption key:
   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```
3. Set `CLONE_ENCRYPTION_KEY` to that generated value in your hosting environment.
4. Keep the exact same key across every restart and redeployment. If you lose
   or change it, the bot cannot decrypt existing clone tokens after restart.
5. Ensure `MONGO_DB_URI` points to a working MongoDB database, then restart.

Clone tokens are encrypted before they are stored in MongoDB. The key must be
kept private and must never be committed to GitHub or included in logs.

### Transport and limitations

This Python implementation uses Pyrogram/Kurigram-compatible client connections
for each clone rather than KustMusic's Bot API webhook endpoint. It therefore
does not require a public `WEBHOOK_URL`; each clone connects through the
Telegram client library. All registered music handlers are attached to clone
clients, and client-context routing makes API replies use the bot that received
the update. PyTgCalls assistant sessions and playback state remain shared by
the running application. Queue state is keyed by chat ID, so all bot identities
in the same chat see the same queue.

Clones are in-memory runtime clients. Their tokens and ownership metadata are
persisted in MongoDB, and clients are restored on startup. Active voice calls
and the currently playing media stream are not guaranteed to survive a process
restart; only clone registration is restored automatically. Validate this on
your target host before relying on it in production.
