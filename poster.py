# poster.py

import os
from datetime import datetime
from utils.logger import logger

def queue_for_zenno(bot_name, filename, text, base_folder="output"):
    """
    Saves a .txt file to output/{bot_name}/{filename}.
    ZennoPoster will monitor this folder to post the content.
    """
    try:
        folder = os.path.join(base_folder, bot_name)
        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(folder, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text.strip())

        logger.info(f"[{bot_name}] ✅ Queued for ZennoPoster: {filepath}")
    except Exception as e:
        logger.error(f"[{bot_name}] ❌ Failed to queue file {filename}: {e}")
