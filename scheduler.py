import time
import schedule
from dotenv import load_dotenv
from main import main
import yaml
from utils.logger import logger

def get_interval_from_config():
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config.get("scheduler", {}).get("interval_seconds", 300)
    except Exception as e:
        logger.error(f"Failed to load schedule interval from config.yaml: {e}")
        return 300  # fallback to 5 min

def run_scheduler():
    load_dotenv()
    interval = get_interval_from_config()
    logger.info(f"🔁 Scheduler started. Interval = {interval} seconds")

    schedule.every(interval).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
