 Memecoin Watcher Bot

A Python-based bot that automatically tracks new memecoins on the Solana and Ethereum blockchains, applies basic filtering, generates tweet-ready content (meme launches, charts, exchange updates, commentary), and can optionally post via multiple Twitter accounts (e.g. through ZennoPoster). It also supports Telegram-based notifications & moderation.

Before running the bot, copy `.env.example` to `.env` and fill in your API keys and other credentials.

---

## 🚀 Features

- **Token Discovery**  
  Fetches new memecoin data from public APIs (Pump.fun, Birdeye, Dexscreener, Alchemy/Infura, etc.).

- **Basic Filtering**  
  Filters tokens by:
  - Minimum liquidity (USD)  
  - Minimum 1-hour trading volume (USD)  
  - Token age (e.g. ≥ 10 minutes)  
  - Blacklisted keywords (e.g. “scam”, “rug”, “test”)  
  - Deployer reputation (via Etherscan)

- **Content Generation (Content Rotation)**  
  For each run, the bot cycles through four types of posts:Add commentMore actions
  1. **Chart** – A 24-hour Bitcoin price chart saved as .png.  
  2. **Exchange Update** – A text summary of a major token’s price and 24h change (e.g. ETH), saved as .txt.  
  3. **Memecoin Launch** – Three separate text posts (.txt) about top new tokens (filtered by liquidity/volume).  
  4. **Commentary/Meme** – A short, engaging remark or meme-style comment (.txt).  

- **Queue for Posting**  
  Generated files (.png and .txt) are placed into `output/{bot_name}/`.
  If `BOT_MODE` is set to `draft` and Telegram credentials are provided,
  they go to `pending/{bot_name}/` instead and you receive a Telegram
  notification. A separate engine (e.g. ZennoPoster) can pick them up
  after approval.

- **Multi-Account Support**  
  Designed to rotate posts across multiple Twitter/X accounts. Each account simply has its own subfolder under output/ (e.g. output/solana_bot_1/, output/eth_bot_2/).

- **Telegram Notifications & Moderation (Optional)**  
  If you supply a Telegram bot token and admin chat ID, anytime a new *.txt appears in pending/{bot_name}/, the bot will send you a message with option buttons:
  - **✅ Publish** – moves that .txt into output/{bot_name}/ so ZennoPoster picks it up.  
  - **🗑 Reject** – deletes the file.

- **Extensible & Modular**  
  You can easily add a Flask web UI for manual edits, or extend filtering logic (pools/holders, social cross-mentions, early adopters, etc.).

---

## 📁 Project Structure

memecoin-watcher-bot/
├── main.py                     # Entry point: drives the content cycle
├── generate_content.py         # Chart, exchange, memecoin, commentary generators
├── reputation_checker.py       # Basic “deployer reputation” checks (Etherscan)
├── poster.py                   # queue_for_zenno(account_name, text) → saves .txt to output
├── telegram_bot.py             # (Optional) Sends Telegram notifications & moderates posts
├── scheduler.py                # Runs main.py on a fixed schedule (using `schedule`)
├── config.yaml                 # Filter & behavior settings
├── .env.example                # Template for environment variables (API keys, tokens)
├── .gitignore                  # Files/folders to ignore in Git commits
├── requirements.txt            # Python dependencies
└── utils/
    └── logger.py               # Centralized logging configuration

/accounts/                       # Example input files (one per Twitter account, if needed)
    └── solana_bot_1.txt        # (Optional) Can store account‐specific templates or data

/output/                         # Generated output; each subfolder = one Twitter account
    ├── solana_bot_1/           # ZennoPoster scans here for new .png/.txt to publish
    └── eth_bot_2/

/pending/                        # Generated .txt land here first (Telegram mod)  
    ├── solana_bot_1/           # Telegram bot notifies you of new files in this folder
    └── eth_bot_2/

/logs/
    └── bot.log                 # Application logs (timestamped)

/utils/
    └── logger.py               # Sets up Python logging to `logs/bot.log`


---

## 📦 Installation

1. **Clone the repository**  
   
bash
   git clone https://github.com/IvanDeFi/memecoin-watcher-bot.git
   cd memecoin-watcher-bot


2. **Install Python dependencies**  
   
bash
   pip install -r requirements.txt


3. **Copy the environment template**  
   
bash
   cp .env.example .env


4. **Open .env and fill in your own keys/tokens** (see next section).

---

## ⚙️ Configuration

### 1. .env (Environment Variables)

Create a local .env file (do **NOT** commit this to GitHub). Populate it with your own credentials:

env
# ----- Telegram (optional) -----
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# ----- Blockchain & Data APIs -----
PUMP_FUN_API_KEY=your_pumpfun_api_key
BIRDEYE_API_KEY=your_birdeye_api_key
DEXSCREENER_API_KEY=your_dexscreener_api_key
ALCHEMY_API_KEY=your_alchemy_api_key      # For Ethereum data (or INFURA_API_KEY)
INFURA_API_KEY=your_infura_api_key

# Reputation Checker (Ethereum)
ETHERSCAN_API_KEY=your_etherscan_api_key

# ----- Bot Behavior Settings -----
BOT_MODE=post                    # "post" → publish via ZennoPoster
                                # "draft" → save to pending/ and notify Telegram
SCHEDULE_INTERVAL=300            # In seconds (300 = 5 minutes)
LOG_LEVEL=info                   # Fallback logging level if not set in config.yaml

# ----- Multi-Account Support -----
TWITTER_ACCOUNTS=solana_bot_1,eth_bot_2   # Comma-separated account folder names

# ----- Proxy Settings (if needed) -----
USE_PROXY=false
PROXY_LIST=proxies.txt           # Path to a file with one proxy URL per line

# ----- Paths (override defaults if desired) -----
OUTPUT_BASE_FOLDER=output
LOG_FILE=logs/bot.log


> **Note:**  
> - Leave any unused variables blank or unset.  
> - The .env file is already listed in .gitignore, so it will not be accidentally pushed to GitHub.

---

### 2. config.yaml (Filter & Behavior Settings)

Example config.yaml in the repository root:

yaml
filters:
  min_liquidity_usd: 2000         # Minimum liquidity in USD for new tokens
  min_volume_1h_usd: 1000         # Minimum 1-hour trading volume (USD)
  min_token_age_minutes: 10       # Token must be at least 10 minutes old
  blacklist_tokens:
    - scam
    - rug
    - test                       # Reject any token whose name contains these substrings
  check_deployer: true            # Enable deployer reputation check via Etherscan
  min_reputation_score: 5         # Minimum reputation score (0–10)

telegram:
  bot_token: ""                   # (Optional) override BOT_TOKEN from .env
  admin_chat_id: 0                # (Optional) override CHAT_ID from .env

output:
  base_folder: "output"           # Base folder where content is saved
  bot_names:
    - "solana_bot_1"
    - "eth_bot_2"

scheduler:
  interval_seconds: 300           # Run `main.py` every 5 minutes

logging:
  level: "info"                   # Logging verbosity (overrides LOG_LEVEL)


> **Tip:** Adjust the numeric thresholds and blacklists as you see fit for your risk tolerance.

---

## 🚀 How It Works (Content Rotation)

Below is a step-by-step description of how each run of main.py (or scheduler.py) produces and queues content.

### 1. Content Rotation Steps (6-Post Cycle)

On each run, the bot reads a small JSON file named state.json to determine which content type to generate next (cycling through 6 types in order). The order is:

1. **Chart**  
   - Fetch 24-hour BTC price data from CoinGecko (or Binance API).  
   - Plot a line chart using Matplotlib (timestamps vs. price).  
   - Save as chart_{YYYYMMDD_HHMM}.png in output/{bot_name}/.

   
python
   from pycoingecko import CoinGeckoAPI
   import matplotlib.pyplot as plt
   from datetime import datetime
   import os

   BASE_OUTPUT = f"output/{bot_name}"

   def generate_and_queue_chart():
       os.makedirs(BASE_OUTPUT, exist_ok=True)
       cg = CoinGeckoAPI()
       data = cg.get_coin_market_chart_by_id("bitcoin", vs_currency="usd", days=1)
       prices = data["prices"]  # [[timestamp, price], ...]
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
       filepath = os.path.join(BASE_OUTPUT, filename)
       plt.savefig(filepath)
       plt.close()
       print(f"✅ Chart generated: {filepath}")


2. **Exchange Update**  
   - Request the current price + 24 h % change for ETH from CoinGecko (or Binance).  
   - Format a simple text snippet, e.g.:
     
📢 ETH price is $1,800.23 (24h: +2.45%)

   - Save as exchange_{YYYYMMDD_HHMM}.txt in output/{bot_name}/.

   
python
   from pycoingecko import CoinGeckoAPI
   from datetime import datetime
   import os

   BASE_OUTPUT = f"output/{bot_name}"

   def generate_and_queue_exchange_info():
       os.makedirs(BASE_OUTPUT, exist_ok=True)
       cg = CoinGeckoAPI()
       data = cg.get_price(ids="ethereum", vs_currencies="usd", include_24hr_change="true")
       price = data["ethereum"]["usd"]
       change = data["ethereum"]["usd_24h_change"]

       text = f"📢 ETH price is ${price:.2f} (24h: {change:+.2f}%)"
       filename = datetime.now().strftime("exchange_%Y%m%d_%H%M.txt")
       filepath = os.path.join(BASE_OUTPUT, filename)
       with open(filepath, "w", encoding="utf-8") as f:
           f.write(text)
       print(f"✅ Exchange info generated: {filepath}")


3. **Memecoin Launch** (three consecutive posts)  
   - Call fetch_new_tokens("solana") + fetch_new_tokens("ethereum") from your parser/ modules. Each returns a list of tokens with fields:  
     
python
     {
       "ticker": "DOGEPEPE",
       "liquidity": 5000,
       "volume_30m": 40000,
       "age_minutes": 15,
       "contract_address": "0x...",
       "deployer": "0xCreatorAddress"
     }

   - Apply filtering rules:
     - liquidity ≥ filters.min_liquidity_usd  
     - volume_30m ≥ filters.min_volume_1h_usd  
     - age_minutes ≥ filters.min_token_age_minutes  
     - Token name does not contain any blacklist_tokens substring  
     - If check_deployer = true, call reputation_checker.is_token_valid(token)  
   - Sort the remaining tokens by 30-minute volume (descending) and pick the top 3.  
   - For each of those 3 tokens, generate a tweet snippet like:
     
🔥 New memecoin on Solana: $DOGEPEPE — 40,000 USD in last 30m! 🚀 #Solana #Memecoin

   - Save each as memecoin_{YYYYMMDD_HHMM}.txt under output/{bot_name}/.

   
python
   from datetime import datetime
   import os

   BASE_OUTPUT = f"output/{bot_name}"

   def generate_and_queue_memecoin_tweet():
       os.makedirs(BASE_OUTPUT, exist_ok=True)
       # Example token (replace with real fetch + filtering logic):
       sample_token = {"ticker": "DOGEPEPE", "volume_30m": 40000, "chain": "Solana"}
       tweet_text = (
           f"🔥 New memecoin on {sample_token['chain']}: "
           f"${sample_token['ticker']} — {sample_token['volume_30m']:,}$ in last 30m! 🚀"
       )
       filename = datetime.now().strftime("memecoin_%Y%m%d_%H%M.txt")
       filepath = os.path.join(BASE_OUTPUT, filename)
       with open(filepath, "w", encoding="utf-8") as f:
           f.write(tweet_text)
       print(f"✅ Memecoin tweet generated: {filepath}")


4. **Commentary / Meme**  
   - Choose a random “meme-style” comment from a preloaded list:
     
python
     comments = [
         "🐸 Chart looks like it's heading Moonward! 🚀",
         "🔮 Could this be the next big gem? Keep an eye on the charts!",
         "👀 DeFi whales are lurking… stay cautious. 🐋",
         "📊 That dip looks like a bull trap to me!",
     ]

   - Save into comment_{YYYYMMDD_HHMM}.txt in output/{bot_name}/.

   
python
   import random
   from datetime import datetime
   import os

   BASE_OUTPUT = f"output/{bot_name}"
   comments = [
       "🐸 Chart looks like it's heading Moonward! 🚀",
       "🔮 Could this be the next big gem? Keep an eye on the charts!",
       "👀 DeFi whales are lurking… stay cautious. 🐋",
       "📊 That dip looks like a bull trap to me!",
   ]

   def generate_and_queue_comment():
       os.makedirs(BASE_OUTPUT, exist_ok=True)
       text = random.choice(comments)
       filename = datetime.now().strftime("comment_%Y%m%d_%H%M.txt")
       filepath = os.path.join(BASE_OUTPUT, filename)
       with open(filepath, "w", encoding="utf-8") as f:
           f.write(text)
       print(f"✅ Comment generated: {filepath}")


After generating these six items (chart, exchange update, 3 memecoin posts, commentary), the cycle resets and repeats on the next scheduled run.

---

### 2. Queue for Posting via ZennoPoster

1. Configure a ZennoPoster project to **monitor** output/{bot_name}/.  
2. On each iteration, ZennoPoster:
   - **Lists all files** (*.png and *.txt), sorts them by timestamp or filename.  
   - Picks the **first file** in lexicographic order:  
     - If it ends with .png, treat it as an image tweet.  
     - If it ends with .txt, read its text and post a tweet.  
   - After posting, **rename or move** that file into output/{bot_name}/sent/ to avoid reposting.  
   - Insert a **random delay** (e.g. 5–10 seconds) between posts to mimic human behavior.  

> **Why ZennoPoster?**  
> - ZennoPoster emulates real browser interactions (clicks, typing, scrubbing), uses cookies, can rotate proxies, and bypass Twitter API rate limits.  
> - It can run dozens of threads, each with its own account profile.

---

### 3. Telegram Notifications & Manual Moderation (Optional)

If you prefer manual oversight:

1. Start the Telegram bot:
   
bash
   python telegram_bot.py

2. Whenever `generate_content.py` places a new file into `pending/{bot_name}/`
   (this happens when `BOT_MODE=draft`), the bot sends you a message with inline buttons:
   
🆕 New post ready for solana_bot_1:
   pending/solana_bot_1/memecoin_20250606_1230.txt

   [✅ Publish]  [🗑 Reject]

3. Press **✅ Publish** to:
   - Move that .txt from pending/{bot_name}/ → output/{bot_name}/  
   - ZennoPoster will see it and post it automatically.  
   Press **🗑 Reject** to delete the file permanently.

python
# Example snippet (telegram_bot.py)
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackQueryHandler
import os

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
ADMIN_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))

def notify_pending(bot_name, filepath):
    text = f"🆕 New post ready for *{bot_name}*:
`{filepath}`"
    keyboard = [
        [
            InlineKeyboardButton("✅ Publish", callback_data=f"publish|{bot_name}|{filepath}"),
            InlineKeyboardButton("🗑 Reject", callback_data=f"reject|{bot_name}|{filepath}")
        ]
    ]
    bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

def callback_handler(update: Update, context):
    query = update.callback_query
    action, bot_name, path = query.data.split("|")
    if action == "publish":
        dest = f"output/{bot_name}/{os.path.basename(path)}"
        os.replace(path, dest)
        bot.send_message(ADMIN_CHAT_ID, f"✅ Published: `{dest}`", parse_mode="Markdown")
    elif action == "reject":
        os.remove(path)
        bot.send_message(ADMIN_CHAT_ID, f"🗑 Rejected: `{path}`", parse_mode="Markdown")
    query.answer()

if __name__ == "__main__":
    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    updater.start_polling()
    updater.idle()


---

### 4. Logging

All processing steps and errors are recorded via a centralized logger (utils/logger.py). By default, logs are written to logs/bot.log.

python
# utils/logger.py
import logging
import os
import yaml

os.makedirs("logs", exist_ok=True)

with open("config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

level = cfg.get("logging", {}).get("level") or os.getenv("LOG_LEVEL", "INFO")

logger = logging.getLogger("memecoin-watcher")
logger.setLevel(level.upper())

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("logs/bot.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


In main.py or any module, use:
python
from utils.logger import logger

logger.info("This is an info message")
logger.error("This is an error message")


---

## 🏗 Running the Bot

1. **Manual Run (One Cycle)**  
   
bash
   python main.py

   - Generates exactly one content item based on the current cycle position (chart → exchange → memecoin → memecoin → memecoin → comment → repeat).

2. **Scheduled Run (Every 5 Minutes)**  
   
bash
   python scheduler.py


## 🧪 Testing

The repository includes a small test suite in `tests/`. Run it with:

```bash
pip install -r requirements.txt  # installs pytest and other dependencies
pytest
```

   - Uses the schedule library to call main() every SCHEDULE_INTERVAL seconds (default = 300s).
   - Keeps the content rotation running indefinitely.

3. **Telegram Moderation**  
   
bash
   python telegram_bot.py

   - Listens for inline button presses (Publish/Reject) to move or delete files in pending/{bot_name}/.

4. **ZennoPoster**  
   - Create a ZennoPoster project that:
     1. Monitors output/solana_bot_1/ (and similarly output/eth_bot_2/).  
     2. On each loop, picks the first .png or .txt.  
        - If .png, upload it as an image tweet.  
        - If .txt, read its content and post a text tweet.  
     3. Renames or moves the file to sent/ subfolder after success:
        
output/solana_bot_1/sent/chart_20250606_1230.png
        output/solana_bot_1/sent/memecoin_20250606_1240.txt

     4. Adds a random delay (5–10 seconds) between posts.

---

## 🔧 Installation & Setup Checklist

1. **Clone + Install**  
   
bash
   git clone https://github.com/IvanDeFi/memecoin-watcher-bot.git
   cd memecoin-watcher-bot
   pip install -r requirements.txt


2. **Environment Variables**  
   
bash
   cp .env.example .env
   # Edit .env to add your own keys & tokens


3. **Verify Directory Structure**  
   
/memecoin-watcher-bot
     ├── main.py
     ├── generate_content.py
     ├── reputation_checker.py
     ├── poster.py
     ├── telegram_bot.py
     ├── scheduler.py
     ├── config.yaml
     ├── .env.example
     ├── requirements.txt
     ├── .gitignore
     └── utils/
         └── logger.py
     └── accounts/
         └── solana_bot_1.txt    # (optional placeholders)
     └── output/
         ├── solana_bot_1/
         └── eth_bot_2/
     └── pending/
         ├── solana_bot_1/
         └── eth_bot_2/
     └── logs/
         └── bot.log


4. **Fill .env**  
   - Add your Telegram bot token & chat ID  
   - Add your Pump.fun, Birdeye, Dexscreener, Alchemy/Infura, Etherscan keys  
   - Set any other flags (BOT_MODE, SCHEDULE_INTERVAL, etc.)

5. **Run**  
   - (Optional) Start the Telegram moderation bot:  
     
bash
     python telegram_bot.py

   - Start the scheduler (continuous operation):  
     
bash
     python scheduler.py


---

## 🛡 Security & Best Practices

- **Never commit** your real .env or any file containing private API keys.  
- Confirm .gitignore includes:
  
.env
  output/
  logs/
  __pycache__/

- Periodically rotate keys (especially for Etherscan, Alchemy/Infura).  
- If using proxies, store them in proxies.txt (and also ignore that file in Git).  
- Run on a secure VPS (Windows, if using ZennoPoster) or Linux (for pure Python/Flask/Telegram).

---

## 💬 Support & Contributions

If you run into issues or have feature ideas, please open an issue or pull request:

👉 [GitHub Issues & PRs](https://github.com/IvanDeFi/memecoin-watcher-bot)

For quick discussion or questions, find me on Telegram: [@Mr_Robot_7_7_7](https://t.me/Mr_Robot_7_7_7)

## License

This project is licensed under the [MIT License](LICENSE).


---

**Thank you for using Memecoin Watcher Bot!** 🚀  
Feel free to customize the cycle, filters, and posting mechanism to suit your needs.
This project monitors new memecoins on Ethereum and Solana and prepares tweet content for bot accounts.
