# reputation_checker.py
import os
import requests
from utils.logger import logger

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def is_token_valid(token):
    if token.get("chain") != "Ethereum":
        return True  # пока проверяем только Ethereum

    deployer = token.get("deployer")
    if not deployer or deployer == "unknown":
        logger.warning("Token missing deployer address.")
        return False

    score = get_deployer_reputation(deployer)
    logger.info(f"Reputation score for {deployer} = {score}")
    return score >= int(os.getenv("MIN_REPUTATION_SCORE", 5))

def get_deployer_reputation(address):
    try:
        # Пример: получаем количество контрактов, созданных этим адресом
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&apikey={ETHERSCAN_API_KEY}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()

        txs = data.get("result", [])
        contract_creations = [tx for tx in txs if tx.get("to") == "" or tx.get("contractAddress")]
        score = 10 - len(contract_creations)  # Чем меньше — тем лучше
        return max(0, min(score, 10))
    except Exception as e:
        logger.error(f"Reputation check failed: {e}")
        return 0
