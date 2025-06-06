# utils/logger.py

import os
import logging

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Initialize logger
logger = logging.getLogger("memecoin-watcher")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

# Formatter for log messages
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# File handler for writing to logs/bot.log
file_handler = logging.FileHandler("logs/bot.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console handler to print logs to stdout
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
