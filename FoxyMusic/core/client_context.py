# ─────「 𝐅ᴏxʏ 」─────
#    Official Project Source
# ────────────────────────
"""Context-aware Telegram client routing for main bot and cloned bot clients.

Plugin handlers are shared between clients. This context variable makes existing
plugin code use the client that received the update without mutating global
module variables (which would race when multiple clones are active).
"""
from contextlib import contextmanager
from contextvars import ContextVar

_active_client = ContextVar("foxy_active_telegram_client", default=None)
_main_client = None
_chat_clients = {}


def set_main_client(client):
    global _main_client
    _main_client = client


def remember_chat_client(chat_id, client):
    if chat_id is not None and client is not None:
        _chat_clients[int(chat_id)] = client


def forget_client(client):
    for chat_id, owner in list(_chat_clients.items()):
        if owner is client:
            _chat_clients.pop(chat_id, None)


def client_for_chat(chat_id):
    if chat_id is not None:
        client = _chat_clients.get(int(chat_id))
        if client is not None:
            return client
    return _main_client


def get_client():
    """Return the client bound to this handler/task, falling back to main."""
    client = _active_client.get()
    return client if client is not None else _main_client


@contextmanager
def client_context(client, chat_id=None):
    if chat_id is not None:
        remember_chat_client(chat_id, client)
    token = _active_client.set(client)
    try:
        yield
    finally:
        _active_client.reset(token)
