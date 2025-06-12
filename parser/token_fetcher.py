# parser/token_fetcher.py
import requests
from datetime import datetime, timezone
from utils.logger import logger

def fetch_from_pumpfun(limit=20):
    url = "https://pump.fun/api/token/list"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        tokens = []
        for item in data[:limit]:
            tokens.append({
                "ticker": item.get("ticker", "???"),
                "liquidity": item.get("liquidity", 0),
                "volume_30m": item.get("volume_30m", 0),
                "age_minutes": calc_age_minutes(item.get("launchUnix")),
                "contract_address": item.get("id"),
                "chain": "Solana",
                "source": "Pump.fun",
                "deployer": item.get("creator", "unknown")
            })
        return tokens
    except Exception as e:
        logger.error(f"Pump.fun fetch failed: {e}")
        return []

def fetch_from_birdeye(limit=20):
    url = "https://public-api.birdeye.so/public/tokenlist?sort_by=volume_1h"
    headers = {"X-API-KEY": "YOUR_BIRDEYE_API_KEY"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json().get("data", [])

        tokens = []
        for item in data[:limit]:
            tokens.append({
                "ticker": item.get("symbol", "???"),
                "liquidity": item.get("liquidity", 0),
                "volume_30m": item.get("volume_1h", 0),
                "age_minutes": 999,  # API may not support timestamp
                "contract_address": item.get("address"),
                "chain": item.get("chain", "Solana"),
                "source": "Birdeye",
                "deployer": "N/A"
            })
        return tokens
    except Exception as e:
        logger.error(f"Birdeye fetch failed: {e}")
        return []

def calc_age_minutes(unix_timestamp):
    if not unix_timestamp:
        return 999
    try:
        now = datetime.now(timezone.utc)
        token_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        age = (now - token_time).total_seconds() / 60
        return int(age)
    except:
        return 999

def get_combined_tokens():
    tokens = []
    tokens.extend(fetch_from_pumpfun())
    tokens.extend(fetch_from_birdeye())
    return tokens
