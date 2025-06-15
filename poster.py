# poster.py

import os
from utils.logger import logger
from utils.settings import (
    get_bot_mode,
    get_output_base_folder,
    has_telegram,
)
from telegram_bot import notify_pending

def queue_for_zenno(bot_name, filename, text, base_folder=None):
    """
    Saves a .txt file to output/{bot_name}/{filename}.
    ZennoPoster will monitor this folder to post the content.
    """
    try:
        if base_folder is None:
            base_folder = get_output_base_folder()
        if get_bot_mode() == "draft" and has_telegram():
            base_folder = "pending"

        folder = os.path.join(base_folder, bot_name)
        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(folder, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text.strip())

        logger.info(f"[{bot_name}] ✅ Queued for ZennoPoster: {filepath}")
        if base_folder == "pending":
            notify_pending(bot_name, filepath)
    except Exception as e:
        logger.error(f"[{bot_name}] ❌ Failed to queue file {filename}: {e}")
