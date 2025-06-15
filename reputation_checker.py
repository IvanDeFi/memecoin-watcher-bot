# reputation_checker.py

import os
import requests
from typing import Optional
from utils.logger import logger

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def is_token_valid(token: dict, min_reputation_score: Optional[int] = None) -> bool:
    """
    Checks if a token's deployer is reputable based on Etherscan data.
    Currently applies only to Ethereum tokens.

    Returns True if:
    - The chain is not Ethereum (skip check)
    - The deployer has a good reputation score (>= threshold)
    """
    if token.get("chain", "").lower() != "ethereum":
        return True  # Only Ethereum tokens are checked

    deployer = token.get("deployer")
    if not deployer or deployer == "unknown":
        logger.warning("Token missing deployer address.")
        return False

    score = get_deployer_reputation(deployer)
    logger.info(f"[Reputation] {deployer} scored {score}/10")

    if min_reputation_score is None:
        min_score = int(os.getenv("MIN_REPUTATION_SCORE", "5"))
    else:
        min_score = int(min_reputation_score)

    return score >= min_score

def get_deployer_reputation(address: str) -> int:
    """
    Estimates deployer reputation based on number of contracts created.

    Logic: fewer contract deployments = higher trust.
    Score = 10 - number of contract deployments (capped between 0–10)
    """
    try:
        url = (
            f"https://api.etherscan.io/api"
            f"?module=account&action=txlist"
            f"&address={address}&apikey={ETHERSCAN_API_KEY}"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        txs = data.get("result", [])
        contract_creations = [
            tx for tx in txs if tx.get("to") == "" or tx.get("contractAddress")
        ]
        score = 10 - len(contract_creations)
        return max(0, min(score, 10))

    except Exception as e:
        logger.error(f"Failed to retrieve deployer reputation: {e}")
        return 0
