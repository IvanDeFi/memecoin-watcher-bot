import requests
from typing import List, Dict, Any

from utils.logger import logger


def fetch_new_tokens(chain: str) -> List[Dict[str, Any]]:
    """Fetch recently created tokens on the given chain.

    The function queries a public API such as Dexscreener or Birdeye and
    normalises the response into a list of dictionaries with the fields
    documented in the README.
    """
    chain_l = chain.lower()

    if chain_l == "solana":
        url = "https://public-api.birdeye.so/defi/trending"
        params = {"timeRange": "30m", "chain": "solana"}
    elif chain_l == "ethereum":
        url = "https://api.dexscreener.com/latest/dex/tokens/ethereum"
        params = {"sort": "txns30m"}
    else:
        raise ValueError(f"Unsupported chain: {chain}")

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:  # pragma: no cover - network failures
        logger.error(f"Failed to fetch tokens for {chain}: {exc}")
        return []

    raw_tokens = data.get("data") or data.get("tokens") or []

    tokens: List[Dict[str, Any]] = []
    for item in raw_tokens:
        token = {
            "ticker": item.get("symbol")
            or item.get("tokenSymbol")
            or item.get("baseTokenSymbol"),
            "liquidity": item.get("liquidity") or item.get("liquidityInUsd"),
            "volume_30m": item.get("volume_30m") or item.get("volume30m"),
            "age_minutes": item.get("age_minutes")
            or item.get("ageMinutes")
            or item.get("age"),
            "contract_address": item.get("address")
            or item.get("tokenAddress")
            or item.get("baseTokenAddress"),
            "deployer": item.get("deployer") or item.get("creator") or "unknown",
            "chain": chain_l,
        }
        tokens.append(token)

    return tokens
