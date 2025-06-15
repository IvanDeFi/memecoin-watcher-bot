import os
import sys
import types

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Stub external dependencies so generate_content imports without them
sys.modules.setdefault("pycoingecko", types.ModuleType("pycoingecko"))
sys.modules["pycoingecko"].CoinGeckoAPI = object

matplotlib = types.ModuleType("matplotlib")
plt = types.ModuleType("pyplot")
setattr(matplotlib, "pyplot", plt)
plt.figure = lambda *a, **k: None
plt.plot = lambda *a, **k: None
plt.title = lambda *a, **k: None
plt.xlabel = lambda *a, **k: None
plt.ylabel = lambda *a, **k: None
plt.xticks = lambda *a, **k: None
plt.tight_layout = lambda *a, **k: None
plt.savefig = lambda path, *a, **k: open(path, "wb").close()
plt.close = lambda *a, **k: None
matplotlib.use = lambda *a, **k: None
sys.modules.setdefault("matplotlib", matplotlib)
sys.modules.setdefault("matplotlib.pyplot", plt)

# Minimal YAML stub for config loading
yaml_mod = types.ModuleType("yaml")
def _safe_load(stream):
    return {
        "filters": {
            "min_liquidity_usd": 2000,
            "min_volume_1h_usd": 1000,
            "min_token_age_minutes": 10,
            "blacklist_tokens": ["scam"],
            "min_reputation_score": 5,
        }
    }
yaml_mod.safe_load = lambda s: _safe_load(s)
sys.modules.setdefault("yaml", yaml_mod)

import utils.settings as settings
settings._config_cache = None

# Stub internal modules that rely on external services
fetcher = types.ModuleType("token_fetcher")
sample_tokens = [
    {"ticker": "GOOD", "liquidity": 3000, "volume_30m": 2000, "age_minutes": 20, "chain": "solana"},
    {"ticker": "BADSCAM", "liquidity": 3000, "volume_30m": 2000, "age_minutes": 20, "chain": "solana"},
    {"ticker": "LOWVOL", "liquidity": 3000, "volume_30m": 500, "age_minutes": 20, "chain": "solana"},
    {"ticker": "YOUNG", "liquidity": 3000, "volume_30m": 2000, "age_minutes": 5, "chain": "solana"},
    {"ticker": "LOWLIQ", "liquidity": 1000, "volume_30m": 2000, "age_minutes": 20, "chain": "solana"},
]
fetcher.fetch_new_tokens = lambda chain: sample_tokens
sys.modules["parser.token_fetcher"] = fetcher

reputation = types.ModuleType("reputation_checker")
called_scores = []
def _is_valid(token, min_score=None):
    called_scores.append(min_score)
    return True
reputation.is_token_valid = _is_valid
sys.modules["reputation_checker"] = reputation

poster_mod = types.ModuleType("poster")
posted = []
def _queue(bot_name, filename, text, base_folder="output"):
    posted.append({"bot": bot_name, "filename": filename, "text": text})
poster_mod.queue_for_zenno = _queue
sys.modules["poster"] = poster_mod

logger_mod = types.ModuleType("logger")
logger_mod.logger = types.SimpleNamespace(info=lambda *a, **k: None,
                                          warning=lambda *a, **k: None,
                                          error=lambda *a, **k: None)
sys.modules["utils.logger"] = logger_mod

from generate_content import sanitize_filename_component, generate_and_queue_memecoin_tweet


def test_sanitize_filename_component():
    text = "token name$%_.123"
    result = sanitize_filename_component(text)
    assert result == "tokenname_123"


def test_generate_and_queue_memecoin_tweet_filters(tmp_path, monkeypatch):
    # Ensure output folder is isolated
    monkeypatch.chdir(tmp_path)
    (tmp_path / "config.yaml").write_text("stub")

    generate_and_queue_memecoin_tweet("bot1", chain="solana", top_n=3)

    # Only one token should pass filters
    assert len(posted) == 1
    assert "GOOD" in posted[0]["filename"].upper()
    # is_token_valid called with configured min score
    assert called_scores == [5]
