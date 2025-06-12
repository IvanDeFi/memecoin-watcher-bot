# poster.py
import os
from datetime import datetime
from utils.logger import logger

def queue_for_zenno(bot_name, filename, text, base_folder="output"):
    folder = os.path.join(base_folder, bot_name)
    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    logger.info(f"[{bot_name}] Queued for ZennoPoster: {filepath}")
