import os
import logging

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("memecoin-watcher")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("logs/bot.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
