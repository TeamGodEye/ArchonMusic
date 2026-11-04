# FoxyMusic — KustMusic-style Clone Integration Notes

## Implemented in this package

- `FoxyMusic/core/client_context.py`
  - Context-local routing makes existing plugin code use the Telegram bot client that received the update.
  - Remembers the last bot client used in each chat so PyTgCalls end-of-stream events can post the next-track UI through the expected bot.

- `FoxyMusic/core/clone_manager.py`
  - Starts and stops dynamic bot clients using the existing Kurigram/Pyrogram-compatible API.
  - Reuses registered handlers and their filters.
  - Stores a SHA-256 token fingerprint as MongoDB `_id`; the token itself is Fernet-encrypted at rest.
  - Restores registered clone clients on startup and supports restart recovery.
  - Limits each non-owner to five registered clones.
  - Avoids registering selected owner/operations-only handlers on clone clients.

- `FoxyMusic/plugins/bot/clone.py`
  - `/clone BOT_TOKEN`
  - `/clones`
  - `/unclone BOT_TOKEN`
  - Main-owner-only `/unclone @username`
  - Main-owner-only `/resetclones`
  - Removes token-bearing command messages when possible and warns against sending tokens in groups.

- `FoxyMusic/__main__.py`
  - Restores clones only after the plugins and PyTgCalls update handlers have loaded.
  - Stops clone clients during graceful shutdown.

- `FoxyMusic/core/call.py` and existing plugin/helper modules
  - Routes existing `app.*` API calls through the active client context so clones can use the existing handlers without mutating shared module globals.

- `config.py`, `sample.env`, `app.json`, `requirements.txt`, `pyproject.toml`, and `README.md`
  - Add `CLONE_ENCRYPTION_KEY`, the cryptography dependency, and setup instructions.

## Shared queue behaviour

The existing FoxyMusic queue is a global in-memory dictionary in `FoxyMusic.misc.db`, keyed by chat ID. All clone clients in the same running process use the same dictionary and existing playback engine. Therefore, commands in the same group share the same queue; different chat IDs keep separate queues.

## Important transport difference from KustMusic

KustMusic's Go implementation routes Bot API updates through per-clone webhooks. This implementation uses a Pyrogram/Kurigram-compatible client connection for each clone, because the existing Python bot is built around those clients and handlers. It matches the clone-facing behaviour, but it does not reproduce KustMusic's exact webhook transport or require `WEBHOOK_URL`.

## Configuration

Generate a Fernet key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Set it as `CLONE_ENCRYPTION_KEY` in the hosting environment. Keep the same key across restarts and redeployments. If the key is lost or changed, saved clone tokens cannot be decrypted. Do not commit the key or share it publicly.

## Validation performed

- Parsed every Python file with Python's AST parser.
- Ran `compileall` successfully.
- Parsed `app.json` as JSON and `pyproject.toml` as TOML.

## Not runtime-tested here

The environment used for this source edit does not have the Pyrogram/Kurigram package installed and has no live Telegram credentials or MongoDB connection. As a result, no real bot token was started and no live `/clone`, voice-chat playback, restart, or unclone test was performed. Run the included code in a test deployment first, with a disposable BotFather token and test group.

## Current limitation

Clone registration is persisted and restored, but an active voice call or currently playing stream is not guaranteed to resume after a process restart. The existing FoxyMusic queue itself is in-memory; persisting and safely resuming its media entries is a separate change.
