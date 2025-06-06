# main.py

import os
import json
from dotenv import load_dotenv
import yaml

from utils.logger import logger
from generate_content import (
    generate_and_queue_chart,
    generate_and_queue_exchange_info,
    generate_and_queue_memecoin_tweet,
    generate_and_queue_comment
)
# (Optional) if using Telegram notifications:
from telegram_bot import notify_pending  

# Content cycle: chart, exchange, memecoin x3, comment
CONTENT_CYCLE = ["chart", "exchange", "memecoin", "memecoin", "memecoin", "comment"]
STATE_FILE = "state.json"


def load_config():
    """
    Reads config.yaml and returns a dictionary.
    """
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_next_content_type():
    """
    Reads state.json, gets current index, increments by 1 modulo len(CONTENT_CYCLE)
    and returns the content type (string).
    If state.json does not exist, creates it with index=0.
    """
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"index": 0}, f)

    with open(STATE_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        idx = data.get("index", 0)
        content_type = CONTENT_CYCLE[idx % len(CONTENT_CYCLE)]
        data["index"] = (idx + 1) % len(CONTENT_CYCLE)
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    return content_type


def main():
    # 1) Load environment variables
    load_dotenv()
    logger.info("🚀 Memecoin Watcher Bot started.")

    # 2) Load configuration
    try:
        config = load_config()
        logger.info(f"Configuration loaded: {config}")
    except Exception as e:
        logger.error(f"Failed to load config.yaml: {e}")
        return

    # 3) Determine which content type to generate
    ctype = get_next_content_type()
    logger.info(f"Next content type: {ctype}")

    # 4) Generate corresponding content
    try:
        if ctype == "chart":
            generate_and_queue_chart()
        elif ctype == "exchange":
            generate_and_queue_exchange_info()
        elif ctype == "memecoin":
            generate_and_queue_memecoin_tweet()
        elif ctype == "comment":
            generate_and_queue_comment()
        else:
            logger.warning(f"Unknown content type: {ctype}")
    except Exception as e:
        logger.error(f"Error while generating '{ctype}': {e}")

    # 5) (Optional) Check pending folder and notify via Telegram
    # Example: new .txt files in pending/{bot_name}/ can trigger notify_pending(bot_name, filepath)

    logger.info("Run complete.\n")


if __name__ == "__main__":
    main()
