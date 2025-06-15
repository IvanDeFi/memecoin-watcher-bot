import time
import schedule
from dotenv import load_dotenv
from main import main
from utils.logger import logger
from utils.settings import get_config

def get_interval_from_config():
    """Return the scheduler interval in seconds from config."""
    try:
        config = get_config()
        return config.get("scheduler", {}).get("interval_seconds", 300)
    except Exception as e:
        logger.error(f"Failed to load schedule interval from config.yaml: {e}")
        return 300  # fallback to 5 min

def run_scheduler():
    """Continuously run scheduled executions of the bot."""
    load_dotenv()
    interval = get_interval_from_config()
    logger.info(f"🔁 Scheduler started. Interval = {interval} seconds")

    schedule.every(interval).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
