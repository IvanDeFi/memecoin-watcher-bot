import os
import logging
import yaml

os.makedirs("logs", exist_ok=True)


def _get_log_level() -> str:
    """Determine log level from config.yaml or environment."""
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        level = config.get("logging", {}).get("level")
        if level:
            return level
    except Exception:
        pass
    return os.getenv("LOG_LEVEL", "INFO")


logger = logging.getLogger("memecoin-watcher")
logger.setLevel(_get_log_level().upper())

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("logs/bot.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
