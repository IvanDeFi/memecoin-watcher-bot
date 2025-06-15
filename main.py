# main.py
import os
import json
from dotenv import load_dotenv
from utils.settings import get_config

from utils.logger import logger
from generate_content import (
    generate_and_queue_chart,
    generate_and_queue_exchange_info,
    generate_and_queue_memecoin_tweet,
    generate_and_queue_comment
)
# Optional: Telegram notification
# from telegram_bot import notify_pending  

DEFAULT_CONTENT_CYCLE = [
    "chart",
    "exchange",
    "memecoin",
    "memecoin",
    "memecoin",
    "comment",
]
STATE_FILE = "state.json"

def load_config():
    """Return bot configuration."""
    return get_config()

def get_next_content_type(content_cycle):
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"index": 0}, f)

    with open(STATE_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        idx = data.get("index", 0)
        content_type = content_cycle[idx % len(content_cycle)]
        data["index"] = (idx + 1) % len(content_cycle)
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    return content_type

def main():
    load_dotenv()
    logger.info("🚀 Memecoin Watcher Bot started.")

    try:
        config = load_config()
    except Exception as e:
        logger.error(f"Failed to load config.yaml: {e}")
        return

    content_cycle = config.get("content_cycle", DEFAULT_CONTENT_CYCLE)
    content_type = get_next_content_type(content_cycle)
    logger.info(f"Generating content: {content_type}")

    bot_names = config.get("output", {}).get("bot_names", [])
    for bot_name in bot_names:
        try:
            if content_type == "chart":
                generate_and_queue_chart(bot_name)
            elif content_type == "exchange":
                generate_and_queue_exchange_info(bot_name)
            elif content_type == "memecoin":
                generate_and_queue_memecoin_tweet(bot_name)
            elif content_type == "comment":
                generate_and_queue_comment(bot_name)
            else:
                logger.warning(f"Unknown content type: {content_type}")
        except Exception as e:
            logger.error(f"[{bot_name}] Failed to generate {content_type}: {e}")

    logger.info("✅ Cycle complete.\n")

if __name__ == "__main__":
    main()
