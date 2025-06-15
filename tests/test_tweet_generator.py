import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tweet_generator import generate_tweet


def test_generate_tweet_basic():
    token = {"chain": "Solana", "ticker": "DOGEPEPE", "volume_30m": 40000}
    tweet = generate_tweet(token)
    assert "DOGEPEPE" in tweet
    assert "Solana" in tweet
    assert "40,000" in tweet
    assert tweet.endswith("#Solana #Memecoin")
