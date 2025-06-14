# parser/solana.py

"""Fetches new Solana tokens using :mod:`parser.token_fetcher`."""

from typing import List, Dict

from utils.logger import logger
from .token_fetcher import fetch_new_tokens


def get_new_tokens() -> List[Dict]:
    """Return a list of newly discovered Solana tokens.

    The function calls :func:`fetch_new_tokens` with the ``solana`` chain and
    logs errors if something goes wrong.

    Returns
    -------
    List[Dict]
        A list of token dictionaries in the unified schema or an empty list on
        failure.
    """

    try:
        tokens = fetch_new_tokens("solana")
        logger.info(f"[solana parser] Retrieved {len(tokens)} tokens")
        return tokens
    except Exception as exc:
        logger.error(f"[solana parser] Failed to fetch tokens: {exc}")
        return []

