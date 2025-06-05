from parser.solana import get_new_solana_tokens
from parser.ethereum import get_new_ethereum_tokens
from tweet_generator import generate_tweet
from poster import post_or_save_tweet
from logger import logger

def main():
    logger.info("Starting Memecoin Watcher Bot")

    solana_tokens = get_new_solana_tokens()
    eth_tokens = get_new_ethereum_tokens()

    top_tokens = (solana_tokens + eth_tokens)[:3]

    for token in top_tokens:
        tweet = generate_tweet(token)
        post_or_save_tweet(tweet)

if __name__ == "__main__":
    main()
