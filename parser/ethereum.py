# parser/ethereum.py

"""Fetches new Ethereum tokens using :mod:`parser.token_fetcher`."""

from typing import List, Dict

from utils.logger import logger
from .token_fetcher import fetch_new_tokens


def get_new_tokens() -> List[Dict]:
    """Return a list of newly discovered Ethereum tokens.

    The function delegates the heavy lifting to :func:`fetch_new_tokens` and
    wraps the call with error handling and logging.

    Returns
    -------
    List[Dict]
        A list of token dictionaries in the unified schema or an empty list on
        failure.
    """

    try:
        tokens = fetch_new_tokens("ethereum")
        logger.info(f"[ethereum parser] Retrieved {len(tokens)} tokens")
        return tokens
    except Exception as exc:
        logger.error(f"[ethereum parser] Failed to fetch tokens: {exc}")
        return []

