# scheduler.py

import schedule
import time
import os
from main import run_main_cycle
from utils.logger import logger

# Load interval from environment or use default (5 minutes)
INTERVAL_SECONDS = int(os.getenv("SCHEDULE_INTERVAL", "300"))

def job():
    logger.info("🔁 Running scheduled cycle")
    run_main_cycle()

def start_scheduler():
    schedule.every(INTERVAL_SECONDS).seconds.do(job)
    logger.info(f"🕒 Scheduler started: every {INTERVAL_SECONDS} seconds")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
