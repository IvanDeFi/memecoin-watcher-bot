"""Utility for formatting memecoin tweets."""

from typing import Dict


def generate_tweet(token: Dict) -> str:
    """Return a formatted tweet text for the provided token.

    Parameters
    ----------
    token: Dict
        Dictionary describing the token. Expected keys include
        ``ticker`` (or ``symbol``), ``chain`` and ``volume_30m``.

    Examples
    --------
    >>> generate_tweet({"chain": "Solana", "ticker": "DOGEPEPE", "volume_30m": 40000})
    '🔥 New memecoin on Solana: $DOGEPEPE — 40,000$ in last 30m! 🚀 #Solana #Memecoin'
    """

    chain = token.get("chain", "").capitalize()
    ticker = token.get("ticker") or token.get("symbol", "UNKNOWN")
    volume = token.get("volume_30m", 0)

    base = (
        f"🔥 New memecoin on {chain}: ${ticker} "
        f"— {volume:,}$ in last 30m! 🚀"
    )

    hashtags = [f"#{chain}" if chain else None, "#Memecoin"]
    hashtags = " ".join(tag for tag in hashtags if tag)

    return f"{base} {hashtags}".strip()
