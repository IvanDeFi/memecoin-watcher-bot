# Technical Questions and Clarifications

Below are clarifying questions that the developer should agree on before starting the work. Each question is followed by an answer.

---

## 1. General Project Goals

### 1.1. Primary Objective  
**Are we building a bot service that runs 24/7 on a Windows-based VDS and posts directly to real Twitter/X accounts?**  
> **Answer:** Yes, the main goal is to deploy an automated bot service on a Windows-based VDS that runs 24/7, continuously monitoring, generating, and publishing crypto content (memecoins, charts, analysis) to real Twitter/X accounts.  
> Posting is handled either directly (via ZennoPoster) or after Telegram moderation. The goal is to simulate the behavior of a real crypto degen or alpha hunter, maintaining content quality and a human-like tone.

### 1.2. Or is this primarily a Proof of Concept / MVP that generates files locally and only simulates posting?  
> **Answer:** Yes, for now this is a Proof of Concept. The goal is to generate and structure content properly — stored in `.txt` files — and simulate how real bots would interact with them.  
> Later, these files will be consumed by ZennoPoster for actual posting.

---

## 2. Target Audience and Scale

### 2.1. How many Twitter/X accounts (bot names) need to be supported in the initial version?
> **Answer:** Start with **two** accounts to validate the workflow.

### 2.2. Do we expect to support dozens of parallel “streams” (e.g., 10–20 accounts), or is it sufficient to start with 1–2?
> **Answer:** For v1, supporting **1–2** accounts is sufficient; scale up later.

---

## 3. MVP vs. Future Enhancements

### 3.1. What features are required for v1?

#### Do we need Telegram-based moderation from day one, or can it be added later?  
> **Answer:** Telegram moderation is important but not critical for launch. In version 1 (v1), it can be postponed if a reliable filter for tokens and posts is in place.  
> However, it will be useful at scale for flexible content control. It's best to architect the system to allow easy integration later.

#### Do we need ZennoPoster integration immediately, or can we use Selenium/requests initially?  
> **Answer:** ZennoPoster integration is crucial for scaling and anti-spam measures, especially when managing multiple accounts.  
> However, for version 1 (v1), Selenium or requests can be used to test the core logic.  
> The key is to structure the code so that ZennoPoster can be integrated easily later.
## 2. Repository Structure and Missing Modules

### 2.1. Parser Modules  
**In the `parser/solana.py` and `parser/ethereum.py` files, there are stubs — what exactly should they return? (list of dicts, which fields?)**  
> **Answer:** Yes, each parser module should return a list of dictionaries, where each dictionary represents a token and includes fields like:  
> - `name`: token name  
> - `symbol`: token ticker  
> - `price`: current price (if available)  
> - `market_cap`: market capitalization  
> - `launch_time`: time of deployment or first transaction  
> - `deploy_address`: deployer address (if applicable)  
> - `scan_url`: link to the blockchain explorer  
>  
> The format may later be converted into a dataclass if we apply strict typing.

**Should we implement the following data sources?**  
- Pump.fun (Solana)  
- Birdeye (Solana)  
- Dexscreener (multi-chain)  
- Alchemy/Infura (Ethereum)  
> **Answer:** For v1 it’s enough to implement two reliable sources:  
> - **Dexscreener** — covers both Solana and Ethereum, returns new token lists with liquidity and volume.  
> - **Alchemy (or Infura)** — for basic token data and deployer info on Ethereum.  
>  
> Optionally, for better Solana accuracy: add Pump.fun or Birdeye.  
>  
> Summary:  
> - **Required:** Dexscreener + Alchemy/Infura  
> - **Optional:** Pump.fun and/or Birdeye for deeper Solana data

**Are credentials or API clients already chosen, or should we analyze which sources are most reliable?**  
> **Answer:** For v1, we’ve pre-selected the following:  
> - **Dexscreener** — public API, no key required  
> - **Alchemy / Infura** — used for Ethereum queries (require `ALCHEMY_API_KEY` or `INFURA_API_KEY`)  
> - **Etherscan** — for deployer reputation (`ETHERSCAN_API_KEY`)  
>  
> For Solana (optional):  
> - **Pump.fun / Birdeye** — require `PUMP_FUN_API_KEY` or `BIRDEYE_API_KEY`  
>  
> These are already listed in `.env.example`. Full reliability analysis can be deferred to v2.

---

### 2.2. `generate_content.py`

**Is `generate_content.py` already present and current, or should it be created from scratch?**  
> **Answer:** Currently, `generate_content.py` is missing. Based on the README, it should be created at the root of the project.  
> It must include the following key functions:  
> - `generate_and_queue_chart()` — generate 24h chart (e.g., BTC or ETH), save as `.png`  
> - `generate_and_queue_exchange_info()` — fetch ETH price/24h change, save as `.txt`  
> - `generate_and_queue_memecoin_tweet()` — parse new memecoins, apply filters, create `.txt` posts  
> - `generate_and_queue_comment()` — generate meme-style comment, save as `.txt`  
>  
> Each function should write to `pending/{bot_name}/` or `output/{bot_name}/`, depending on whether Telegram moderation is active.

**Where should the file be located — root or `utils/`?**  
> **Answer:** `generate_content.py` is core business logic and should reside at the **root** of the project (with `main.py`, `poster.py`, `scheduler.py`).  
> The `utils/` folder is meant for helpers only.

---

### 2.3. `poster.py`

**The current `poster.py` contains `queue_for_zenno(bot_name, text)` — should we also implement direct posting (via Selenium or Twitter API)?**  
> **Answer:** No, direct posting via Selenium or Twitter API is **not required** for v1.  
> We rely on ZennoPoster for posting, so `poster.py` should only enqueue `.txt` / `.png` files into `output/{bot_name}/`.  
>  
> Optionally, you may add:  
> ```python
> def post_direct_via_selenium(bot_name: str, text_filepath: str):
>     # Headless browser logic to post tweet
>     pass
> ```  
> But it’s an optional fallback — not used by default.

**Should `poster.py` read `.txt` files from `output/{bot_name}` and post them, or only enqueue for ZennoPoster?**  
> **Answer:** `poster.py` should **only enqueue** files into `output/{bot_name}/`.  
> Actual posting is done by ZennoPoster, which monitors the folder and publishes in order.
## 4. `tweet_generator.py` vs `generate_content.py`

**The repository still contains `tweet_generator.py`, while the README refers to `generate_content.py`. Which one is canonical?**  
> **Answer:** The canonical module is `generate_content.py`, as it includes the full logic for generating the four content types (charts, exchange updates, memecoin tweets, and comments).  
> `tweet_generator.py` is a deprecated stub and can be removed after migrating any useful template logic it contains into `generate_content.py`.

**Can `tweet_generator.py` be safely deleted, or does it contain logic to preserve?**  
> **Answer:** Yes, it can be deleted — but first migrate any reusable functions, such as:  
> ```python
> def format_memecoin_tweet(token):
>     return f"🔥 New memecoin: ${token.symbol} — {token.volume:,}$ in last 30m!"
> ```  
> Ensure such formatting logic is preserved in `generate_content.py` before deleting.

---

## 5. `scheduler.py`

**It uses the `schedule` library to run `main.py` every N seconds (default: 300). Should cron be supported instead?**  
> **Answer:** No need to build cron logic into the code. The `schedule` library is used for simplicity and local testing.  
> The README should document how to use `cron` externally, for example:  
> ```bash
> */5 * * * * cd /path/to/memecoin-watcher-bot && /usr/bin/python3 main.py
> ```  
> Thus, cron support is handled at the OS level, not in code.

**Should the scheduler support auto-restart after OS reboot (e.g., systemd or Task Scheduler)?**  
> **Answer:** No, `schedule` does not persist after reboot. Auto-restart should be configured via:  
> - `systemd` on Linux  
> - Task Scheduler on Windows  
>  
> Include example configs in the README for both platforms.

---

## 6. Telegram Integration

**The repository has `telegram_bot.py` with `notify_pending`. Should we implement full Telegram moderation (watching `pending/{bot_name}/`)?**  
> **Answer:** For v1, a full moderation flow isn't required. The `notify_pending()` function should scan `pending/{bot_name}/` and send the admin a list of new posts with inline buttons:  
> - ✅ Publish  
> - ❌ Reject  
>  
> On approval, move the file to `output/{bot_name}/`; on rejection, move it to `rejected/{bot_name}/` or delete it. This provides basic human moderation while keeping ZennoPoster as the posting backend.

**Should all posts first be saved to `pending/{bot_name}/`, and then moved to `output/{bot_name}/` after approval?**  
> **Answer:** Yes, the expected workflow is:  
> - Generate `.txt` and `.png` files into `pending/{bot_name}/`  
> - Run `notify_pending()` to send a Telegram message with action buttons  
> - On ✅ Publish → move to `output/{bot_name}/`  
> - On ❌ Reject → move to `rejected/{bot_name}/` or delete  
>  
> This allows manual review of each post before publication.

**Should the Telegram bot offer additional commands like `/start`, `/status`?**  
> **Answer:** Yes. Minimum recommended commands:  
> - `/start` — welcome message with instructions  
> - `/status` — list of pending posts per bot with counts and filenames  
>  
> Optional but useful:  
> - `/help` — list of all available commands  
> - `/approve_all` — publish all pending posts  
> - `/reject_all` — reject all pending posts

**Can we implement inline editing of pending posts before publishing?**  
> **Answer:** Yes, that's a powerful feature. Add an “✏️ Edit” inline button. On click:  
> - Bot sends the current content of the post  
> - User replies with an edited message  
> - Bot updates the file in `pending/{bot_name}/`  
> - Buttons (Publish/Reject) are shown again  
>  
> Optionally support `/edit <filename>` to start editing a specific post via command.
## 3. Configuration (`.env`, `config.yaml`, `.gitignore`)

### 1. `.env` vs `.env.example`

**The `.env.example` template contains many keys (Pump.fun, Birdeye, Dexscreener, Alchemy, Infura, Etherscan). Are all of them required, or just a few?**  
> **Answer:** In v1, not all keys are mandatory. Only the ones for services actually used are required:
> 
> - `DEXSCREENER_API_KEY`: optional (Dexscreener often works without a key)
> - `ALCHEMY_API_KEY` or `INFURA_API_KEY`: required for Ethereum data
> - `ETHERSCAN_API_KEY`: required for deployer reputation checks
> - `PUMP_FUN_API_KEY`, `BIRDEYE_API_KEY`: optional, only if you integrate these sources
>
> So your actual `.env` may contain only:
> ```
> ALCHEMY_API_KEY=...
> ETHERSCAN_API_KEY=...
> ```

**Should we document rate limits for free plans (e.g., CoinGecko 50 req/min vs. Alchemy 333k/mo)?**  
> **Answer:** Yes. Documenting main rate limits helps avoid production issues:
> 
> | Provider      | Limit (Free Tier)                     |
> |---------------|----------------------------------------|
> | CoinGecko     | 50 requests per minute                 |
> | Alchemy       | 333,333/month (~11,111/day)            |
> | Infura        | 100,000/day                            |
> | Etherscan     | 5/sec, 100,000/day                     |
> | Dexscreener   | ~10/sec per IP (no key needed)         |
> | Pump.fun      | 100–200/min (varies)                   |
> | Birdeye       | 100–200/min (varies)                   |
>
> This table should be placed in `README.md` or `docs/RATE_LIMITS.md`. Also, define `api_retry_backoff` in `config.yaml` and add retry logic on HTTP 429 errors.

---

### 2. `config.yaml`

**The example config includes `filters.min_liquidity_usd`, `min_volume_1h_usd`, etc. Are these the only filters?**  
> **Answer:** No. v1 filtering includes multiple criteria:
> 
> - `min_liquidity_usd`
> - `min_volume_1h_usd`
> - `min_token_age_minutes`
> - `blacklist_tokens` — rejects tokens with specific substrings
> - `check_deployer` + `min_reputation_score` — checks deployer trust via Etherscan  
> 
> In v2 you may add more filters like `max_tx_fee_usd`, `min_holder_count`, etc.

**Should blacklist token names be case-insensitive? Does it apply to name, symbol, or address?**  
> **Answer:** Yes, blacklist checks should be case-insensitive and apply to:
> 
> - `name`: full token name (e.g., “BabyShiba”)
> - `symbol`: ticker (e.g., “BSHIB”)
> 
> If either contains a blacklisted substring → token is rejected.  
> Addresses are not filtered — that can be added separately later.

**If `check_deployer: true`, must we only use Etherscan? Or allow alternatives?**  
> **Answer:** No, don’t limit to Etherscan. Use a modular approach:
> 
> - **Etherscan** — widely used but rate-limited  
> - **Alchemy / Infura** — can fetch deployer data  
> - **Blockscout, Axiom** — other explorers  
> - **Solscan, Birdeye** — for Solana  
> 
> Ideally support fallback or aggregation from multiple sources for reliability and deeper analysis.

---

### 3. Multiple Bot Names

**The `output.bot_names` list defines bot names. Should each name match a folder `output/{bot_name}`? Should these be created manually?**  
> **Answer:** Yes. Each `bot_name` corresponds to a subfolder like `output/{bot_name}`.  
> 
> These are used for:
> - storing generated posts
> - pending reviews
> - moderation outputs
> 
> Best practice: auto-create these folders if missing.  
> Add a runtime check in `main.py`, `poster.py`, etc., to ensure folders exist.

---

### 4. Logging

**Logs are written to `logs/bot.log` via `utils/logger.py`. Should we implement log rotation (size/time)?**  
> **Answer:** Not required for v1, but recommended for v2+.  
> 
> For now:  
> - Single file: `logs/bot.log`  
> - Works well in dev/local setups  
> 
> Future:  
> - Add rotation by size (e.g., 5MB) or time (daily)  
> - Use `RotatingFileHandler` from `logging.handlers`  
> 
> Summary:  
> - v1 — OK as-is  
> - v2 — add rotation for long-term stability

**Is log level only taken from `.env` (`LOG_LEVEL`), or should it be overrideable via `config.yaml`?**  
> **Answer:** Currently it uses `.env` → `LOG_LEVEL`.  
> 
> You can add `log_level` override to `config.yaml` for flexibility.
> 
> Recommended order:  
> 1. `config.yaml` → `log_level`  
> 2. fallback → `.env` → `LOG_LEVEL`  
> 
> That gives you env-agnostic flexibility (dev/prod).

---

### 5. `.gitignore`

**We usually ignore:**
```
.env
__pycache__/
output/
logs/
```
**Should we also add `pending/` and `*.pyc`?**  
> **Answer:** Yes, recommended:
> ```
> *.pyc
> pending/
> ```
> 
> - `*.pyc`: auto-generated bytecode, pollutes Git  
> - `pending/`: contains intermediate files, not for versioning

**Should we exclude `state.json`?**  
> **Answer:** Yes, if it’s auto-generated runtime data (like last token ID):
> 
> - Add to `.gitignore`  
> 
> Exception:  
> - If it holds essential config shared between devs, keep it and use `state.example.json` for template  
> 
> Conclusion:  
> ```
> state.json
> ```
---
## 4. Content Cycle and State Management

### 1. `state.json` Format

**It currently contains `{"index": n}`. What happens if `state.json` is corrupted or deleted?**  
> **Answer:** If `state.json` is missing or malformed:
> 
> - Initialize with `index = 0` by default
> - Create a new `state.json` with default content
> - Avoid crashing the bot
> 
> ✅ Recommended handling:
> ```python
> try:
>     with open("state.json", "r") as f:
>         state = json.load(f)
>         index = state.get("index", 0)
> except (FileNotFoundError, json.JSONDecodeError):
>     index = 0
>     with open("state.json", "w") as f:
>         json.dump({"index": index}, f)
> ```
> This ensures fault tolerance and resilience to file corruption.

---

### 2. Content Cycle and Customization

**The current cycle is `["chart","exchange","memecoin","memecoin","memecoin","comment"]`. Is this final? Should it be configurable via `config.yaml`?**  
> **Answer:** This is just a default cycle. It **should be configurable** to support multiple posting strategies per bot/persona.
>
> ✅ Add to `config.yaml`:
> ```yaml
> content_cycle:
>   - chart
>   - exchange
>   - memecoin
>   - memecoin
>   - memecoin
>   - comment
> ```
> Then dynamically load it in your script. This allows flexibility per account (e.g., some bots post more memes, others focus on charts).

---

### 3. Concurrent Access

**If two instances of `main.py` run simultaneously, `state.json` could be corrupted. Should we add file locking or enforce a single instance?**  
> **Answer:** Yes, concurrent writes to `state.json` can cause corruption.
> 
> ✅ Two mitigation strategies:
> 
> - **File locking** (recommended):
>   ```python
>   from filelock import FileLock
>   with FileLock("state.json.lock"):
>       # safely read/write state.json
>   ```
> 
> - **Single instance enforcement**:
>   Only run one instance at a time via `scheduler.py`, cron, or Task Scheduler.
> 
> 📌 Best practice: use **both** locking + scheduled single instance.

---

### 4. `pending/` vs. `output/`

**Where are `.txt` and `.png` files first saved: directly to `output/{bot_name}` or first to `pending/{bot_name}`?**  
> **Answer:** All generated files should first be saved to `pending/{bot_name}`.
>
> ✅ Flow:
> 1. `generate_content.py` creates content
> 2. Saves files to `pending/{bot_name}/`
> 3. `telegram_bot.py` notifies admin with preview
> 4. On "✅ Publish", the file is moved to `output/{bot_name}/`
> 5. `poster.py` (via ZennoPoster) handles posting
>
> 📌 Benefits:
> - Human review and editing
> - Avoids spam or low-quality posts
> - Supports multi-generator workflows

---

### 5. Filename Collision Prevention

**Current format is `"%Y%m%d_%H%M"`. Should we include seconds or a random suffix to avoid overwrites?**  
> **Answer:** Yes, using only minute precision may cause overwrites if two posts are generated within the same minute.
>
> ✅ Safer alternatives:
> - Add seconds: `"%Y%m%d_%H%M%S"`
> - Append random hash: e.g., `uuid4().hex[:6]`
> - Combine both:
>   ```python
>   from uuid import uuid4
>   filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid4().hex[:4]
>   ```
> This ensures uniqueness even in fast loops or parallel runs.
---
## 5. Memecoin Filtering Logic

### 1. Parser Data Schema

**Each parser returns a list of dictionaries. Which fields are mandatory? Example:**
```yaml
{
  "ticker": "DOGEPEPE",
  "contract_address": "0x1234…",
  "volume_30m": 40000,
  "liquidity_usd": 5000,
  "age_minutes": 15,
  "deployer_address": "0xCreator…"
}
```

**Which fields are guaranteed, and which are optional?**  
> **Answer:** Yes, the data schema returned by each parser should be standardized for consistent filtering.

✅ **Required fields** (must be present in every token):
```yaml
{
  "ticker": "DOGEPEPE",
  "contract_address": "0x1234…",
  "liquidity_usd": 5000,
  "volume_30m": 40000,
  "age_minutes": 15
}
```

🟡 **Optional fields** (may be missing, but are helpful if available):
```yaml
{
  "deployer_address": "0xCreator…",   # For deployer check
  "holders": 1423,                    # Number of holders
  "is_verified": true,                # Whether contract is verified
  "symbol": "DOGEPEPE",               # Sometimes distinct from ticker
  "chain": "solana"                   # For multi-chain support
}
```

📌 **Example of a full entry:**
```json
{
  "ticker": "DOGEPEPE",
  "symbol": "DOGEPEPE",
  "contract_address": "0x1234abcde12345abc",
  "volume_30m": 50000,
  "liquidity_usd": 10000,
  "age_minutes": 12,
  "deployer_address": "0x999creator999",
  "holders": 1488,
  "is_verified": true,
  "chain": "ethereum"
}
```

> By clearly separating required and optional fields, the system can support both strict filtering and flexibility across different chains or data sources.

---

### 2. Missing `liquidity_usd`

**If the API doesn’t return `liquidity_usd`, should we calculate it?**  
> **Answer:** If `liquidity_usd` is not available, it can be **estimated** — but only if reliable inputs are present.

🔍 **Conditions to calculate liquidity:**

- If the API provides:
  - `token_reserve` and `base_reserve`, or
  - `token_price` and `pair volume`

📌 **Typical AMM formula (e.g. Uniswap-style pools):**
```python
liquidity_usd = 2 × min(reserve_token × token_price, reserve_base × base_price)
```
This assumes a balanced liquidity pool (equal value on both sides).

✅ **When it makes sense:**

- **Pump.fun** often lacks direct liquidity but may give enough to estimate.
- **DexScreener/Birdeye** may provide price and volume but not always liquidity.

⚠️ **Avoid calculating if:**

- No reserves, prices, or pair data are available.
- The result would be too inaccurate or misleading.

👉 **Recommendation:**

- Estimate liquidity only if accurate source data is available.
- Otherwise, skip the token and optionally log a warning.
## 5. Memecoin Filtering Logic (continued)

### 2. Blacklist (`blacklist_tokens`)

**Example:**  
```yaml
blacklist_tokens: ["scam", "rug", "test"]
```

**Should the search be case-insensitive?**  
**Does the filter apply to name, symbol, or contract address?**  
> **Answer:** Yes, matching should be case-insensitive. Convert both the token’s name/symbol and the blacklist entries to lowercase (e.g. via `.lower()`), so values like “ScAm” match “scam”.

- The filter applies to:
  - `name` — full token name.
  - `symbol` — ticker.
- If **either** contains a blacklist substring, the token is excluded.
- **Contract addresses** are **not** filtered here. Use a separate list for address blocking.

**Should we also match against a blacklist of addresses?**  
> **Answer:** Yes. It's recommended to maintain a separate `address_blacklist` for known malicious contracts.

Benefits:
- Token names and symbols may change; contract addresses do not.
- Useful for catching redeploys of known bad actors.

Example in `config.yaml`:
```yaml
filters:
  blacklist_tokens: ["scam", "rug", "test"]
  address_blacklist:
    - "0xBadContractAddress1..."
    - "0xAnotherBadAddress..."
```

**Filtering logic:**
1. Check if `contract_address` is in `address_blacklist`.
2. If not, check if `name` or `symbol` match any `blacklist_tokens`.

---

### 3. Deployer Reputation Check

**If `check_deployer: false` in `config.yaml`, should we skip it completely?**  
> **Answer:** Yes. If `check_deployer` is `false`, skip the check entirely. `is_token_valid()` should always return `True` in that case.

Example in code:
```python
if not config.filters.check_deployer:
    return True
```

**What if `ETHERSCAN_API_KEY` is missing or invalid?**  
> **Answer:** Log a **warning**, skip the check, and return `True`. Do not block tokens due to unavailable reputation data.

Example:
```python
try:
    result = etherscan_client.get_contract_creator(token.contract_address)
except EtherscanAuthError:
    logger.warning("Etherscan API key missing or invalid, skipping deployer check")
    return True
```

---

### 4. Sorting and Top-3 Selection

**How to break ties in `volume_30m`?**  
> **Answer:** Use multi-level sorting:

- Primary: `volume_30m` (descending)
- Secondary: `liquidity_usd` (descending)
- Tertiary: `age_minutes` (ascending)
- Final: `symbol` alphabetically (or use fixed random seed)

Python example:
```python
tokens_sorted = sorted(
    tokens,
    key=lambda t: (
        -t["volume_30m"],
        -t.get("liquidity_usd", 0),
        t.get("age_minutes", float("inf")),
        t["symbol"].lower()
    )
)
top3 = tokens_sorted[:3]
```

**If fewer than 3 tokens remain after filtering, how many posts to generate?**  
> **Answer:**  
- If 0 tokens → skip memecoin step.  
- If 1 or 2 → generate 1 or 2 tweets.  
- To avoid single-token tweets, consider a config option:
```yaml
min_memecoin_posts: 2
```

---

### 5. Chain Separation (Solana vs Ethereum)

**Should Solana and Ethereum tokens be processed separately?**  
> **Answer:** Yes. Run each parser independently and generate separate top-3 posts per chain.

Benefits:
- Different filters per network
- Clear tweet context (“on Solana” vs. “on Ethereum”)
- Easier scalability (e.g., for BNB, Base, etc.)

**Should we ever merge both pools (Solana + Ethereum)?**  
> **Answer:** No — for clarity and maintainability, keep them separated.

Example in `config.yaml`:
```yaml
memecoin:
  separate_chains: true
```

**Should the tweet explicitly mention the chain (“on Solana”)?**  
> **Answer:** Yes. Always include the chain in the tweet for transparency and user awareness.

Example:
```
🔥 New memecoin on Solana: $DOGEPEPE — 40k USD volume in 30m! #Solana #Memecoin
```

This helps users quickly assess transaction fees, slippage, and DEX.
---
## 6. Chart Generation and Exchange Price Updates

### 1. Data Sources and Fallback Options

**We currently use CoinGecko (via pycoingecko).**

**Should we implement a fallback (e.g., Binance API) if CoinGecko fails?**  
> **Answer:** For v1, a fallback is not required, but highly recommended for better availability.

- **Primary:** CoinGecko — 50 calls per minute.
- **Fallback:** Binance API — fast and reliable for major tokens (rate limit ~1200 calls/minute).

**Fallback logic pattern:**

1. Try CoinGecko.
2. If it fails (HTTP 429, timeout, etc.), log a warning.
3. Retry using Binance.
4. If Binance also fails — return cached value or display "Data unavailable".

**Example:**
```python
try:
    price = cg.get_price(ids="ethereum", vs_currencies="usd")["ethereum"]["usd"]
except Exception:
    logger.warning("CoinGecko failed, falling back to Binance")
    price = binance_client.get_symbol_ticker(symbol="ETHUSDT")["price"]
```

---

**Should we support generating a chart for ETH or other altcoins (configurable)?**  
> **Answer:** Yes. The asset shown in the chart should be configurable in `config.yaml`.

Example:
```yaml
chart:
  symbol: "ethereum"
  vs_currency: "usd"
  days: 1
```

Then in code:
```python
symbol = config.chart.symbol
vs = config.chart.vs_currency
days = config.chart.days
data = cg.get_coin_market_chart_by_id(symbol, vs, days=days)
```

This allows switching to Bitcoin, Solana, or other tokens without changing the code.

---

### 2. Chart Styling Requirements

**Currently we use:**  
```python
plt.plot(timestamps, values)
```

**Should we set a fixed size (e.g., 1200×675 px for Twitter)?**  
> **Answer:** Yes. For Twitter, 16:9 (1200×675 px) is ideal.

Set figure size:
```python
plt.figure(figsize=(12, 6.75), dpi=100)  # → 1200x675 pixels
plt.plot(timestamps, values)
plt.tight_layout()
plt.savefig(output_path)
```

**Make dimensions configurable in `config.yaml`:**
```yaml
chart:
  width_px: 1200
  height_px: 675
  dpi: 100
```

Calculate figsize in code:
```python
figsize = (config.chart.width_px / config.chart.dpi, config.chart.height_px / config.chart.dpi)
```

---

**Do we need grid, fonts, branding colors, or watermark?**  
> **Answer:** For v1, minimal styling is fine.

- **Grid:** Yes — for readability (`plt.grid(True, linestyle='--', alpha=0.5)`).
- **Fonts:** Default is fine, but increase title/axis size.
  ```python
  plt.title("ETH Price", fontsize=16)
  plt.xlabel("Time", fontsize=12)
  plt.ylabel("Price (USD)", fontsize=12)
  ```
- **Brand colors:** Not needed in v1. Add later via config.
- **Watermark:** Optional; can add later for branding or copyright.

Config example:
```yaml
chart_style:
  grid: true
  title_fontsize: 16
  label_fontsize: 12
  use_brand_colors: false
  watermark: false
```

---

**Should the time axis be timezone-aware?**  
> **Answer:** Yes. Use a timezone (e.g., UTC or your locale) so the X-axis is accurate.

Config:
```yaml
chart:
  timezone: "Europe/Moscow"
```

Code:
```python
from datetime import datetime
import pytz
import matplotlib.dates as mdates

tz = pytz.timezone(config.chart.timezone)
dates = [datetime.fromtimestamp(ts, tz) for ts in timestamps]

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M', tz=tz))
```

---

### 3. Exchange Update

**We currently fetch ETH price from CoinGecko:**
```python
data = cg.get_price(ids="ethereum", vs_currencies="usd", include_24hr_change="true")
```

**Should we support multiple tokens (ETH, SOL, etc.)?**  
> **Answer:** Yes. Add a list of tokens in `config.yaml`:

```yaml
exchange:
  tokens:
    - id: "ethereum"
      symbol: "ETH"
    - id: "solana"
      symbol: "SOL"
```

In `generate_and_queue_exchange_info()`:

- Loop through `config.exchange.tokens`.
- For each, fetch price and change:
```python
cg.get_price(ids=id, vs_currencies="usd", include_24hr_change="true")
```

Generate output:
```
ETH: $1,900 (–2.5%)  
SOL: $25 (–1.2%)
```

This offers broader market visibility in one tweet or file.

---

**What if CoinGecko returns None or raises an error?**  
> **Answer:** On error:

1. Log a warning.
2. Try fallback (e.g., Binance).
3. Use cached data if available.
4. If no data — skip or print `Data unavailable`.

Example:
```python
try:
    price_info = cg.get_price(...)
    price = price_info["ethereum"]["usd"]
except Exception as e:
    logger.warning(f"CoinGecko error: {e}. Trying fallback or cached data.")
    price = get_cached_price("ethereum") or "Data unavailable"
```
## 7. Posting Mechanism

### 1. ZennoPoster: Setup and Requirements

**Do we need to include a `.zpproj` ZennoPoster file in the repo?**  
> **Answer:**  
No, including a full `.zpproj` binary file is not required. It may bloat the repo and become outdated.

Instead:

- Create a `ZENNOPOSTER_SETUP.md` with step-by-step instructions:
  - How to create a new project in ZennoPoster.
  - How to set the monitored folder to `output/{bot_name}/`.
  - How to use ZennoPoster’s Credential Manager.
  - How to configure scheduled execution and posting logic.

You *can* include a minimal `.zpproj` template (without credentials) in a `zenno/` folder.

This approach keeps the repo clean while offering helpful guidance.

---

**Where are Twitter logins/passwords stored in ZennoPoster?**  
> **Answer:**  
ZennoPoster uses a built-in **Credentials Manager**:

- Open ZennoPoster → Tools → Credentials Manager.
- Create a new entry (type: Twitter) with username + password or token.
- In your `.zpproj`, use the “Get Credential” block by name.

Credentials are encrypted and not stored in the project file — this protects sensitive data.

---

**Do we need a fallback method (e.g., Selenium) if ZennoPoster is not available?**  
> **Answer:**  
No. We rely **exclusively** on ZennoPoster.  
No fallback using Selenium or Twitter API will be implemented.  
All publishing is handled via ZennoPoster monitoring `output/{bot_name}/`.

---

### 2. Direct Twitter API

**The README says "No Twitter/X API required". What if someone wants to integrate Twitter API v2?**  
> **Answer:**  
Currently, the system does **not** require the Twitter API — all posting is done via ZennoPoster.

---

**Should we add `tweepy` or similar to `requirements.txt`?**  
> **Answer:**  
No — do not add `tweepy` or similar libraries unless Twitter API is officially used.  
This avoids misleading others into thinking API support is built-in.

You may:

- Mention in `README.md` that Twitter API integration is possible via `tweepy`, `twython`, etc.
- Leave a commented-out placeholder in `poster.py` for future integration.

---

### 3. Posting Frequency and Limits

**Currently: one post every 5 minutes → 30 min full cycle. Is that optimal?**  
> **Answer:**  
No — we recommend **low-frequency** posting for v1.

Suggested config:
```yaml
posting_schedule:
  mode: fixed_times        # or interval / disabled
  times: ["08:30", "18:00"]
  timezone: "Europe/Moscow"
  random_offset_minutes: 5
```

This reduces spam risk, looks more human, and only posts high-quality filtered content.

---

**If the bot missed a posting cycle (e.g., due to downtime), how can we catch up?**  
> **Answer:**  
Use `catch_up_mode` to generate and schedule missed content:

```yaml
catch_up_mode:
  enabled: true
  delay_between_posts_seconds: 300
```

Mechanism:

- Check `state.json` for last posted item.
- Calculate how many posts were missed.
- Generate and publish them with delays (to simulate human behavior).

---

### 4. Logic for Multiple Accounts

**How to assign content to specific bots?**  
- Solana → `solana_bot_1`
- Ethereum → `eth_bot_2`
- Or alternate bots regardless of chain?

> **Answer:**  
Use a flexible **bot-to-chain** mapping in `config.yaml`:

```yaml
bot_accounts:
  solana_bot_1:
    chains: ["solana"]
  eth_bot_2:
    chains: ["ethereum"]
  mix_bot_3:
    chains: ["solana", "ethereum"]
```

Logic:

- If a post includes a `chain` (Solana/Ethereum), use only bots assigned to that chain.
- If multiple bots qualify → rotate them via round-robin.
- If no chain → select a bot randomly or cyclically.

This prevents overlapping and gives you control over persona-based content distribution.

---

### 5. Post-Publish File Handling

**Should ZennoPoster move published posts to `output/{bot_name}/sent/`? Should Python clean up old files?**  
> **Answer:**  
Yes. After a post is published, ZennoPoster should **move** it to `sent/`.

Also, Python should **clean up old files** (e.g., older than 7 days).

Config:
```yaml
cleanup_settings:
  enabled: true
  folder: "output/{bot_name}/sent"
  max_age_days: 7
```

---

**If ZennoPoster fails to publish (e.g., network error), should we retry or move the file to `failed/`?**  
> **Answer:**  
On failure, **move the file to `failed/{bot_name}/`**.

Retries should only happen within a separate recovery cycle.

Main loop should **not** retry automatically to avoid duplicates.

Retry support can be added inside `catch_up_mode`, which can:

- Re-publish missed posts
- Insert delay between retries

```yaml
catch_up_mode:
  enabled: true
  delay_between_posts_seconds: 300
```
---
## 8. Telegram Bot & Moderation

### 1. `notify_pending` Implementation

**Where should `pending/{bot_name}` be created?**  
> **Answer:**  
Yes, `generate_content.py` should write all generated `.txt` and `.png` files **directly** to `pending/{bot_name}/`.  
This enables manual review before posting.

---

**After a post is approved (via "Publish"), where should the file go?**  
> **Answer:**  
Move the file **directly to `output/{bot_name}/`**, since this is the folder monitored by ZennoPoster.

Using an intermediate `approved/` folder is unnecessary at this stage, but can be added later if needed.

---

**What happens if a moderator clicks “Reject”?**  
> **Answer:**  
Immediately suggest the next available post from the same `pending/{bot_name}/` queue.

If the queue is empty, optionally **trigger new content generation** (e.g., fetch fresh memecoins).  
This ensures the flow continues smoothly until a post is accepted.

You can support this via the `/next` command or by automatically displaying the next post after rejection.

---

### 2. Telegram Bot Commands

**Are “Publish” and “Reject” buttons enough?**  
> **Answer:**  
They are the **bare minimum**, but we strongly recommend also adding:

- `/next` — Skip current and show the next pending post
- `/edit` — Allow inline text editing before publishing

Additional helpful commands:

- `/start` — Display bot capabilities
- `/status` — Show number of pending posts and their filenames

---

**Do we need `/status`, `/skip`, etc.?**  
> **Answer:**  
Yes. At a minimum:

- `Publish` and `Reject` inline buttons
- `/next` command (or button) — to go to the next post
- `/edit` — for quick inline editing

These give the admin more control and reduce friction during review.

---

### 3. Error Handling and Notifications

**What if the admin clicks “Publish”, but the file was already deleted or moved?**  
> **Answer:**  
Send a clear error message:

```
⚠️ Failed to publish: file no longer exists. Try next one?
```

Then show the `/next` button.  
**Do not** attempt to re-post or recover the missing file — just move forward.

---

**What if `BOT_TOKEN` or `CHAT_ID` are missing in `.env`?**  
> **Answer:**  
Don’t crash. Instead:

- Log a warning:  
  `WARNING: Telegram not configured (BOT_TOKEN or CHAT_ID missing). Skipping notify_pending.`

- Skip Telegram notification logic entirely.

Telegram is **optional**, and the bot should run without it.

---

**Should we send Telegram alerts on generation errors or API issues?**  
> **Answer:**  
Yes. Telegram notifications are useful for:

- API errors (CoinGecko, DEXs, etc.)
- No tokens found after filtering
- Generation failure (e.g., plot crashed)
- Rate limits hit or exceeded

These alerts should go to the admin via Telegram, ideally:

- Immediately if critical (e.g., total failure)
- Grouped/delayed if minor (e.g., no tokens today)

This helps identify silent errors when the bot runs unattended.
---
## 9. Deployment & Environment

### 1. Python Version

**README says “Python 3.9+”. Do we need a specific version like 3.10?**  
> **Answer:**  
No strict version required — Python **3.9 or higher** is sufficient.  
The project has been tested with Python 3.9 and 3.10.  
Avoid using Python 3.11+ until all dependencies are verified for compatibility.

---

**Are there differences between Windows (ZennoPoster) and Linux (pure Python) setups?**  
> **Answer:**  
Yes — important differences:

**On Windows (ZennoPoster):**

- ZennoPoster works **only on Windows**
- Project runs via `.zpproj` template
- Needs access to folders like `output/{bot_name}/`, `logs/`
- Python scripts are launched via `python.exe`
- Use Windows Task Scheduler or `.bat` scripts for automation

**On Linux (pure Python):**

- ZennoPoster not supported
- Use `cron` or `systemd` for scheduling
- Install all dependencies with `pip`
- Great for VPS/VDS deployment
- Can use headless tools (e.g. Selenium) as a fallback

---

### 2. Virtual Environment

**Should we recommend `venv` or `conda`?**  
> **Answer:**  
Use **`venv`**:

- Built into Python (since 3.3)
- Simple, lightweight
- Works on both Windows and Linux
- Compatible with ZennoPoster
- No need for `conda`, which is overkill here

---

**Any Linux system dependencies like `libpng-dev` or `ffmpeg`?**  
> **Answer:**  
Not needed for Windows + ZennoPoster setup.

For Linux devs (e.g. CI/CD):

- `libpng-dev` — required for `matplotlib` image output
- `ffmpeg` — only if video/GIF generation is added

Right now, `pip install -r requirements.txt` is enough.

---

### 3. Service / Daemon Setup

**Should `scheduler.py` run as a system service?**  
> **Answer:**  
Yes. Background mode is recommended:

- **Windows:** use **Task Scheduler** to auto-run `scheduler.py` on boot
- **Linux:** can run as a `systemd` service (optional)

---

**Should we include example configs for systemd / Task Scheduler?**  
> **Answer:**  
Yes, but not mandatory for v1. Helpful for automation:

- Add a `.bat` script to run `scheduler.py` on Windows
- Provide screenshots or step-by-step setup for Task Scheduler
- (Optional) `scheduler.service` file for systemd

Place these in `docs/` or `automation/`.

---

### 4. Secrets Management

**Do we store credentials only in `.env` or support secure secrets too?**  
> **Answer:**  
For MVP — use local `.env` (excluded via `.gitignore`).

In production, consider:

- CI/CD secrets (e.g. GitHub Actions)
- Secret managers: Vault, AWS Secrets Manager, Railway Secrets, etc.

Codebase is easily extensible to support these later.
---
## 10. Error Handling, Logging & Monitoring

### 1. Unhandled Exceptions

**If a generator (chart, exchange, memecoin, comment) fails, should we just log the error and continue?**  
> **Answer:**  
Yes. If `generate_chart()` or another module crashes, we should:

- Log the error using `logger.exception(...)`
- Continue to the next content type

This ensures fault tolerance — one failure won't crash the whole cycle.

```python
try:
    generate_memecoin()
except Exception as e:
    logger.exception("Error while generating memecoin")
```

---

**Should we send a Telegram alert if a generator fails?**  
> **Answer:**  
Yes — especially in production. Send a Telegram alert to notify the admin.

Example:
```python
notify_admin(f"❌ Generation error in generate_memecoin: {str(e)}")
```

Optionally add throttling (e.g. no more than 1 alert/hour per generator) to avoid spam.

---

**Should we retry on temporary errors like API timeouts?**  
> **Answer:**  
Yes — retry **1–2 times** on:

- Timeouts
- 5xx errors
- Temporary rate limits

Use **exponential backoff** (e.g., 2s → 4s → fail) to reduce pressure on APIs and avoid infinite loops.

---

### 2. Log Rotation & Retention

**Logs go to `logs/bot.log`. Should we rotate logs (e.g. 10MB or daily)?**  
> **Answer:**  
Yes — log rotation is recommended to prevent large files and disk overflow.

Use **size-based** (e.g. 10 MB) or **time-based** (e.g. daily) rotation.

---

**Should we use `logging.handlers.RotatingFileHandler`?**  
> **Answer:**  
Yes — this is the standard and stable solution.

- Built into Python
- Handles size-based rotation
- Supports backups (`backupCount`)

Example:

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler("logs/bot.log", maxBytes=10_000_000, backupCount=5)
```

---

### 3. Monitoring & Alerts

**Besides Telegram, do we need Slack or email notifications?**  
> **Answer:**  
No — **Telegram is sufficient** for v1:

- Fastest to set up
- Easy to integrate with Python
- Familiar for most teams

---

**If the bot stops running, how do we detect it?**  
> **Answer:**  
To detect silent crashes, we recommend:

- Send “🟢 Bot started” on launch
- Add a **keepalive ping**, e.g. once a day:
  “📣 Bot is active — no issues detected”

This acts as a heartbeat, letting you know the bot is still alive.
---
## 11. Dependencies & Versions

### 1. `requirements.txt`

**Current file:**
```
requests
python-dotenv
pyyaml
schedule
selenium
matplotlib
pycoingecko
python-telegram-bot
```

---

**Should we pin exact version ranges (e.g. `pycoingecko>=2.0.0,<3.0.0`)?**  
> **Answer:**  
Yes — pinning versions helps ensure reproducibility and avoids breaking changes when libraries are updated. Suggested constraints:

```txt
requests>=2.25.0,<3.0.0  
python-dotenv>=0.21.0,<1.0.0  
pyyaml>=5.4,<7.0  
schedule>=1.1.0,<2.0.0  
selenium>=4.0.0,<5.0.0  
matplotlib>=3.3.0,<4.0.0  
pycoingecko>=2.0.0,<3.0.0  
python-telegram-bot>=13.0,<21.0
```

---

**Are we actively using Selenium, and do we need to specify browser + driver versions (e.g., Chrome 112 + ChromeDriver 112)?**  
> **Answer:**  
No — Selenium is currently **not required**. The actual publishing logic is handled via **ZennoPoster**.

Selenium may be used in the future for testing or fallback automation, but for v1, we do **not** need to specify browser or driver versions.

---

**Do we need to add `tweepy` (or any Twitter SDK)?**  
> **Answer:**  
No. Since we use **ZennoPoster** for all Twitter publishing (not the official Twitter API), there's no need to add tweepy or any SDK.

If we decide to support Twitter API in the future, we can introduce `tweepy` or `twython` at that point.

---

### 2. Future Libraries

**Should we add `Flask` now for a potential web UI?**  
> **Answer:**  
No — a web interface is **not part of v1**. Telegram moderation and file-based workflows are sufficient.

If we build a dashboard in the future (e.g., for managing posts or logs), we can then add `Flask` or `FastAPI`.

---

**Should we plan for a database (e.g., SQLite or PostgreSQL)?**  
> **Answer:**  
No DB is needed now. We use:

- `.txt` files for posts
- `state.json` for status tracking
- `.env` for secrets

This is sufficient for MVP. If later we want post history, moderation logs, or user tracking, we can evaluate:

- SQLite — simple, file-based
- PostgreSQL — scalable, for cloud or multi-user environments

For now: **Keep It Simple.**
---
## 12. Testing & QA

### 1. Unit & Integration Tests

**Are tests expected to be written? Should API responses be mocked (e.g., `pycoingecko`, parsers)?**  
> **Answer:**  
Not required for MVP, but strongly recommended for scaling or multi-developer environments.  
At minimum:
- Mock external APIs (CoinGecko, Birdeye, Etherscan) to prevent rate-limits.
- Use `pytest` + `unittest.mock` or `responses` for mocking.

---

**Should we create a `tests/` directory with templates?**  
> **Answer:**  
Optional for v1, but highly recommended to prepare for test coverage.  
You can add:
- `tests/test_generate_content.py` — basic checks
- `tests/test_filters.py` — mock filtering logic
- Use `pytest` as the standard runner

This structure will help onboard contributors and prepare for future CI/CD pipelines.

---

### 2. Manual QA

**How to manually check chart/exchange/memecoin/comment generation?**  
> **Answer:**  
Run `generate_content.py` in debug mode or with a CLI flag:

```bash
python generate_content.py --type chart
```

The script will:
- Save output in `pending/{bot_name}/` as `.txt` and `.png`
- Optionally, trigger `notify_pending()` to send the draft to Telegram
- Allow preview and moderation before publishing

---

**Should we include mock “dry” data for offline testing?**  
> **Answer:**  
Yes. It’s helpful to include mock files to simulate API responses. Example:

```
mock_data/
├── solana_sample.json
├── eth_sample.json
├── coingecko_eth_response.json
```

This allows:
- Local testing without internet
- Avoiding API quotas
- Testing rare edge cases (e.g., zero tokens, huge volume, missing fields)

---

### 3. Edge Cases

**What if no new tokens were launched recently (e.g. last 10 minutes)?**  
> **Answer:**  
Gracefully skip the memecoin generation and log the event.  
Optional Telegram alert:
```
📭 No new tokens found in the last 10 minutes. Skipping memecoin step.
```

---

**Should we skip memecoin and continue with comment generation?**  
> **Answer:**  
Yes. If no valid tokens are available (empty list or all filtered), the bot should:
- Log the event
- Skip `generate_memecoin()`
- Move to the next generator, like `generate_comment()`

This ensures smooth operation during low-activity periods.
---
## 13. Documentation & Code Practices

### 1. Comments and Docstrings

**Are PEP 257-style docstrings required for all functions?**  
> **Answer:**  
Yes — all public functions and classes should include PEP 257-compliant docstrings.  
This improves readability and maintainability for all developers.  
Priority files:
- `generate_content.py`
- `poster.py`
- `parser/`
- `telegram_bot.py`

---

### 2. README Completeness

**README already includes setup — do we need videos, diagrams, or screenshots?**  
> **Answer:**  
The current README covers all key instructions, but we plan to add:
- 📊 A project structure diagram
- 🎬 A “Getting Started” video (optional)
- 📸 Screenshots for ZennoPoster or CLI usage  
These will improve UX for non-technical contributors and simplify onboarding.

## 14. Security & Compliance

### 1. API Key Permissions

**What access rights and limits apply for each provider (Pump.fun, Birdeye, Dexscreener, Alchemy/Infura, Etherscan)?**  
> **Answer:** Each API provider has its own restrictions and limits. Summary:

| Provider      | Free Tier Limits                 | Required Access Type           |
|---------------|----------------------------------|--------------------------------|
| Pump.fun      | Undocumented, may need cookies   | Public GET only                |
| Birdeye       | 1,000 req/day (free), paid tiers | Public token/market data       |
| Dexscreener   | Public API, basic rate limiting  | Read-only, no auth             |
| Alchemy       | 330K req/mo (free)               | Project key for RPC access     |
| Infura        | 100K req/day (free)              | Project ID for Ethereum RPC    |
| Etherscan     | 5 req/sec, 100K/day (free)       | Read contract/token info       |

- 🔒 Always store sensitive credentials in `.env`
- ❌ Never commit `.env` to GitHub
- ✅ Recommended: exclude `.env` in `.gitignore`

---

**Are there IP whitelist or CORS limitations?**  
> **Answer:**  
Yes, for some providers like Alchemy/Infura/Etherscan:
- **IP Whitelist**: available in paid plans; add your server IP if needed.
- **CORS**: not relevant for backend (Python) scripts. Only applies if we add a frontend (e.g., Flask) in the future.

---

### 2. Rate Limit Handling

**Should we back off on 429 (Too Many Requests) responses from Alchemy?**  
> **Answer:**  
Yes — implement exponential backoff with retry logging.  
If the issue persists, skip the failing token temporarily and continue the cycle.

---

**If 429 errors become frequent, should the cycle be slowed down?**  
> **Answer:**  
Yes — dynamically increase the wait time or reduce the number of API queries per cycle to stay under rate limits.  
This avoids full pipeline blockage during high activity periods.

---

### 3. Data Privacy

**Are any personal credentials (usernames/passwords) stored in the system?**  
> **Answer:**  
🔒 No — personal login data (e.g., Twitter passwords) is never handled by the Python bot.  
ZennoPoster manages them securely within its encrypted account system.  
The `.env` only contains API and bot tokens.

---

**Do we need to encrypt `.env` or add extra protections?**  
> **Answer:**  
🔐 Not required, but:
- Always exclude `.env` from Git.
- Restrict filesystem permissions (e.g., 600 on Linux).
- Store secrets securely in CI/CD pipelines if needed later.



