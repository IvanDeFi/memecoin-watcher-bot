import os
from datetime import datetime
import random
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt
import yaml

from parser.token_fetcher import fetch_new_tokens
from reputation_checker import is_token_valid
from poster import queue_for_zenno
from utils.logger import logger


def generate_and_queue_chart(bot_name):
    """Generate a BTC price chart and queue it for posting."""
    logger.info(f"[{bot_name}] Generating BTC chart")
    cg = CoinGeckoAPI()
    data = cg.get_coin_market_chart_by_id("bitcoin", vs_currency="usd", days=1)
    prices = data["prices"]

    timestamps = [p[0] for p in prices]
    values = [p[1] for p in prices]

    plt.figure(figsize=(6, 4))
    plt.plot(timestamps, values)
    plt.title("BTC Price Last 24h")
    plt.xlabel("Timestamp")
    plt.ylabel("Price (USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    filename = datetime.now().strftime("chart_%Y%m%d_%H%M.png")
    out_path = os.path.join("output", bot_name, filename)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    plt.close()
    logger.info(f"[{bot_name}] Chart saved: {out_path}")


def generate_and_queue_exchange_info(bot_name):
    """Queue a short ETH market update for posting."""
    logger.info(f"[{bot_name}] Generating ETH exchange info")
    cg = CoinGeckoAPI()
    data = cg.get_price(ids="ethereum", vs_currencies="usd", include_24hr_change="true")
    price = data["ethereum"]["usd"]
    change = data["ethereum"]["usd_24h_change"]

    text = f"📢 ETH price is ${price:.2f} (24h: {change:+.2f}%)"
    filename = datetime.now().strftime("exchange_%Y%m%d_%H%M.txt")
    queue_for_zenno(bot_name, filename, text)


def sanitize_filename_component(text):
    return "".join(c for c in text if c.isalnum() or c == "_")


def generate_and_queue_memecoin_tweet(bot_name, chain="solana", top_n=3):
    """Post about trending memecoins on the specified chain."""
    logger.info(f"[{bot_name}] Fetching memecoins on {chain}")

    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        filters = config.get("filters", {})
    except Exception as e:
        logger.error(f"[{bot_name}] Failed to load filters from config.yaml: {e}")
        filters = {}

    min_liq = filters.get("min_liquidity_usd", 0)
    min_vol = filters.get("min_volume_1h_usd", 0)
    min_age = filters.get("min_token_age_minutes", 0)
    blacklist = [b.lower() for b in filters.get("blacklist_tokens", [])]
    min_rep = filters.get("min_reputation_score", 5)

    tokens = fetch_new_tokens(chain)

    def passes_filters(token):
        if token.get("liquidity", 0) < min_liq:
            return False
        if token.get("volume_30m", 0) < min_vol:
            return False
        if token.get("age_minutes", 0) < min_age:
            return False
        ticker = token.get("ticker", "").lower()
        if any(bl in ticker for bl in blacklist):
            return False
        return is_token_valid(token, min_rep)

    valid_tokens = [t for t in tokens if passes_filters(t)]

    top_tokens = sorted(valid_tokens, key=lambda t: t["volume_30m"], reverse=True)[:top_n]

    for token in top_tokens:
        tweet = (
            f"🔥 New memecoin on {chain.capitalize()}: ${token['ticker']} "
            f"— {token['volume_30m']:,}$ in last 30m! 🚀"
        )
        safe_ticker = sanitize_filename_component(token['ticker'])
        filename = datetime.now().strftime(
            f"memecoin_{safe_ticker}_%Y%m%d_%H%M.txt"
        )
        queue_for_zenno(bot_name, filename, tweet)
        logger.info(f"[{bot_name}] Generated post for ${token['ticker']}")


def generate_and_queue_comment(bot_name):
    """Queue a random meme-like comment for posting."""
    logger.info(f"[{bot_name}] Generating meme-style comment")
    comments = [
        "🐸 Chart looks like it's heading Moonward! 🚀",
        "🔮 Could this be the next big gem? Keep an eye on the charts!",
        "👀 DeFi whales are lurking… stay cautious. 🐋",
        "📊 That dip looks like a bull trap to me!",
    ]
    text = random.choice(comments)
    filename = datetime.now().strftime("comment_%Y%m%d_%H%M.txt")
    queue_for_zenno(bot_name, filename, text)
