# memecoin-watcher-bot
# 🧠 Memecoin Watcher Bot — Solana & Ethereum

A smart bot that monitors **new memecoins** on **Solana and Ethereum** and auto-generates tweet content.

## 📌 What the bot does:

1. Tracks new token launches using APIs (Birdeye, Pump.fun, Dexscreener, DEXTools, etc.)
2. Collects important token data: name, ticker, contract, liquidity, volume
3. Generates a tweet (funny, factual, or meme-style)
4. Posts the tweet automatically (or saves it)

## ⚙️ Requirements:

- Python 3.9+
- APIs used:
  - [Pump.fun](https://pump.fun)
  - [Birdeye](https://birdeye.so)
  - [Dexscreener](https://docs.dexscreener.com/)
  - [Alchemy / Infura for Ethereum](https://www.alchemy.com/)
- No Twitter/X API required (headless browser or local save is enough)

## 🧪 Test Task for Developers

Please submit a simple Python script that does the following:

1. Fetches a list of new tokens from **Pump.fun** or similar source
2. Picks top 3 tokens by liquidity or volume
3. Generates tweet-like text, such as:

   > "🔥 New memecoin launched on Solana: $DOGEPEPE — 40k volume in 20 min! Is this the next SHIBA? 🐶🚀 #Solana #Memecoin"

4. Saves the tweet text to a file `output/tweet.txt`

If you can complete this task — you’re likely a great fit. 🙌

## 📁 Project Structure (suggested)

