import os
try:
    import yaml
except Exception:  # pragma: no cover - optional dependency
    yaml = None

_config_cache = None


def get_config() -> dict:
    """Return configuration loaded from ``config.yaml``.

    The file is read only once and cached for subsequent calls.
    """
    return _load_config()

def _load_config():
    global _config_cache
    if _config_cache is None:
        try:
            if yaml is None:
                raise ImportError
            with open("config.yaml", "r", encoding="utf-8") as f:
                _config_cache = yaml.safe_load(f) or {}
        except Exception:
            _config_cache = {}
    return _config_cache

def get_bot_mode() -> str:
    cfg = _load_config()
    return os.getenv("BOT_MODE") or cfg.get("bot_mode", "post")

def get_output_base_folder() -> str:
    cfg = _load_config()
    return cfg.get("output", {}).get("base_folder", "output")

def has_telegram() -> bool:
    cfg = _load_config()
    token = os.getenv("TELEGRAM_BOT_TOKEN") or cfg.get("telegram", {}).get("bot_token")
    chat_id = os.getenv("TELEGRAM_CHAT_ID") or str(cfg.get("telegram", {}).get("admin_chat_id"))
    return bool(token) and bool(chat_id) and chat_id != "0"
