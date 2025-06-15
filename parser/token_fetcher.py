# parser/token_fetcher.py
import os
import requests
from datetime import datetime, timezone
from utils.logger import logger

PUMP_FUN_API_KEY = os.getenv("PUMP_FUN_API_KEY")
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")

# Default timeout for all outgoing API requests (in seconds)
REQUEST_TIMEOUT = 10


def fetch_new_tokens(chain: str):
    """
    Fetches recent memecoins from public APIs.
    Supported chains: "solana", "ethereum".
    Returns a list of tokens with unified structure.
    """
    if chain.lower() == "solana":
        return fetch_solana_tokens()
    elif chain.lower() == "ethereum":
        return fetch_ethereum_tokens()
    else:
        logger.warning(f"[fetch_new_tokens] Unsupported chain: {chain}")
        return []


def fetch_solana_tokens():
    try:
        url = "https://client-api.pump.fun/tokens/trending"
        headers = {"x-api-key": PUMP_FUN_API_KEY} if PUMP_FUN_API_KEY else {}
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        tokens = []
        for item in data:
            created_at = datetime.fromisoformat(item["createdAt"].replace("Z", "+00:00"))
            age_minutes = (datetime.now(timezone.utc) - created_at).total_seconds() / 60

            tokens.append({
                "ticker": item.get("ticker", "UNKNOWN"),
                "liquidity": item.get("liquidity", 0),
                "volume_30m": item.get("volume", 0),
                "age_minutes": int(age_minutes),
                "contract_address": item.get("id", ""),
                "deployer": "unknown",
                "chain": "Solana"
            })

        logger.info(f"Fetched {len(tokens)} Solana tokens")
        return tokens

    except requests.Timeout:
        logger.error("Failed to fetch Solana tokens: request timed out")
        return []
    except Exception as e:
        logger.error(f"Failed to fetch Solana tokens: {e}")
        return []


def fetch_ethereum_tokens():
    try:
        url = "https://public-api.birdeye.so/public/tokenlist?chain=ethereum"
        headers = {"X-API-KEY": BIRDEYE_API_KEY} if BIRDEYE_API_KEY else {}
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json().get("data", {}).get("tokens", [])

        tokens = []
        for item in data:
            tokens.append({
                "ticker": item.get("symbol", "UNKNOWN"),
                "liquidity": item.get("liquidity", 0),
                "volume_30m": item.get("volume", 0),
                "age_minutes": 999,  # Age is unknown in this API
                "contract_address": item.get("address", ""),
                "deployer": item.get("creator", "unknown"),
                "chain": "Ethereum"
            })

        logger.info(f"Fetched {len(tokens)} Ethereum tokens")
        return tokens

    except requests.Timeout:
        logger.error("Failed to fetch Ethereum tokens: request timed out")
        return []
    except Exception as e:
        logger.error(f"Failed to fetch Ethereum tokens: {e}")
        return []
