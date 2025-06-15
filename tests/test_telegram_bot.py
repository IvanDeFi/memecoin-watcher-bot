import os
import sys
import types
import importlib

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set env so telegram_bot initializes
os.environ["TELEGRAM_BOT_TOKEN"] = "token"
os.environ["TELEGRAM_CHAT_ID"] = "42"

# Stub telegram modules
sent_messages = []

class DummyBot:
    def __init__(self, token=None):
        self.token = token
    def send_message(self, chat_id, text, reply_markup=None, parse_mode=None):
        sent_messages.append({
            "chat_id": chat_id,
            "text": text,
            "reply_markup": reply_markup,
            "parse_mode": parse_mode,
        })

telegram_mod = types.ModuleType("telegram")
telegram_mod.Bot = DummyBot
telegram_mod.InlineKeyboardButton = lambda text, callback_data: {"text": text, "callback_data": callback_data}
telegram_mod.InlineKeyboardMarkup = lambda kb: {"keyboard": kb}
telegram_mod.Update = object
sys.modules.setdefault("telegram", telegram_mod)

telegram_ext_mod = types.ModuleType("telegram.ext")
telegram_ext_mod.Updater = object
telegram_ext_mod.CallbackQueryHandler = lambda func: None
telegram_ext_mod.CallbackContext = object
sys.modules.setdefault("telegram.ext", telegram_ext_mod)

# Stub dotenv so module imports cleanly
dotenv_mod = types.ModuleType("dotenv")
dotenv_mod.load_dotenv = lambda: None
sys.modules.setdefault("dotenv", dotenv_mod)

import telegram_bot
importlib.reload(telegram_bot)


def test_notify_pending_sends_message():
    sent_messages.clear()
    telegram_bot.notify_pending("bot1", "/x/y/post.txt")
    assert sent_messages
    msg = sent_messages[0]
    assert msg["chat_id"] == 42
    assert "post.txt" in msg["text"]
    assert "bot1" in msg["text"]
    kb = msg["reply_markup"]["keyboard"]
    assert kb[0][0]["callback_data"] == "publish|bot1|post.txt"
    assert kb[0][1]["callback_data"] == "reject|bot1|post.txt"


def test_handle_callback_publish_and_reject(monkeypatch):
    moves = []
    deletes = []
    monkeypatch.setattr(telegram_bot.shutil, "move", lambda s, d: moves.append((s, d)))
    monkeypatch.setattr(telegram_bot.os, "makedirs", lambda p, exist_ok=False: None)
    monkeypatch.setattr(telegram_bot.os, "remove", lambda p: deletes.append(p))

    sent_messages.clear()
    upd = types.SimpleNamespace(callback_query=types.SimpleNamespace(data="publish|bot2|file.txt", answer=lambda: None))
    telegram_bot.handle_callback(upd, None)
    assert moves == [(os.path.join("pending", "bot2", "file.txt"), os.path.join("output", "bot2", "file.txt"))]
    assert "Published" in sent_messages[-1]["text"]

    sent_messages.clear()
    upd = types.SimpleNamespace(callback_query=types.SimpleNamespace(data="reject|bot2|file.txt", answer=lambda: None))
    telegram_bot.handle_callback(upd, None)
    assert deletes == [os.path.join("pending", "bot2", "file.txt")]
    assert "Rejected" in sent_messages[-1]["text"]
