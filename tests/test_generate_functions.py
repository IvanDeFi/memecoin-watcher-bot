import os
import sys
import types
from datetime import datetime

import pytest

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Stub external modules so imports succeed
sys.modules.setdefault("pycoingecko", types.ModuleType("pycoingecko"))
sys.modules["pycoingecko"].CoinGeckoAPI = object

matplotlib = types.ModuleType("matplotlib")
plt = types.ModuleType("pyplot")
setattr(matplotlib, "pyplot", plt)
sys.modules.setdefault("matplotlib", matplotlib)
sys.modules.setdefault("matplotlib.pyplot", plt)

import utils.settings as settings
settings._config_cache = None

# Stub logger to avoid file writes
logger_mod = types.ModuleType("logger")
logger_mod.logger = types.SimpleNamespace(info=lambda *a, **k: None,
                                          warning=lambda *a, **k: None,
                                          error=lambda *a, **k: None)
sys.modules["utils.logger"] = logger_mod

# Stub internal modules that rely on external services
fetcher = types.ModuleType("token_fetcher")
fetcher.fetch_new_tokens = lambda chain: []
sys.modules["parser.token_fetcher"] = fetcher

reputation = types.ModuleType("reputation_checker")
reputation.is_token_valid = lambda token, min_score=None: True
sys.modules["reputation_checker"] = reputation

# Provide minimal YAML stub
yaml_mod = types.ModuleType("yaml")
yaml_mod.safe_load = lambda s: {}
sys.modules["yaml"] = yaml_mod

# Stub telegram bot module used by poster
telegram_bot_mod = types.ModuleType("telegram_bot")
telegram_bot_mod.notify_pending = lambda *a, **k: None
sys.modules.setdefault("telegram_bot", telegram_bot_mod)

# Ensure we load the real poster module, not the stub from other tests
sys.modules.pop("poster", None)

from poster import queue_for_zenno
import generate_content


def test_queue_for_zenno(tmp_path):
    bot = "testbot"
    filename = "note.txt"
    text = "  hello world  "

    queue_for_zenno(bot, filename, text, base_folder=str(tmp_path))

    out_file = tmp_path / bot / filename
    assert out_file.exists()
    assert out_file.read_text(encoding="utf-8") == "hello world"


def test_generate_and_queue_exchange_info(monkeypatch):
    captured = {}

    def fake_queue(bot_name, filename, text):
        captured['bot'] = bot_name
        captured['filename'] = filename
        captured['text'] = text

    class FakeCG:
        def get_price(self, *a, **k):
            return {"ethereum": {"usd": 1234.56, "usd_24h_change": -2.5}}

    fixed_dt = datetime(2023, 1, 2, 3, 4)

    class DummyDT(datetime):
        @classmethod
        def now(cls):
            return fixed_dt

    monkeypatch.setattr(generate_content, "queue_for_zenno", fake_queue)
    monkeypatch.setattr(generate_content, "CoinGeckoAPI", lambda: FakeCG())
    monkeypatch.setattr(generate_content, "datetime", DummyDT)

    generate_content.generate_and_queue_exchange_info("mybot")

    assert captured['bot'] == "mybot"
    assert captured['filename'] == "exchange_20230102_0304.txt"
    assert captured['text'] == "\U0001F4E2 ETH price is $1234.56 (24h: -2.50%)"


def test_generate_and_queue_memecoin_tweet(monkeypatch, tmp_path):
    tokens = [
        {"ticker": "GOOD1", "volume_30m": 1000, "chain": "Solana"},
        {"ticker": "EVIL$", "volume_30m": 3000, "chain": "Solana"},
        {"ticker": "ANOTHER", "volume_30m": 2000, "chain": "Solana"},
    ]

    monkeypatch.setattr(generate_content, "fetch_new_tokens", lambda c: tokens)
    monkeypatch.setattr(generate_content, "is_token_valid", lambda t, m=None: True)

    monkeypatch.setattr(generate_content, "get_config", lambda: {})

    calls = []

    def fake_queue(bot, fname, text):
        calls.append((bot, fname, text))

    fixed_dt = datetime(2023, 1, 2, 3, 4)

    class DummyDT(datetime):
        @classmethod
        def now(cls):
            return fixed_dt

    monkeypatch.setattr(generate_content, "queue_for_zenno", fake_queue)
    monkeypatch.setattr(generate_content, "datetime", DummyDT)

    generate_content.generate_and_queue_memecoin_tweet("bot", chain="solana", top_n=2)

    assert len(calls) == 2
    # tokens sorted by volume: EVIL$, ANOTHER
    assert calls[0][0] == "bot"
    assert calls[0][1] == "memecoin_EVIL_20230102_0304.txt"
    assert calls[0][2].startswith("\U0001F525 New memecoin on Solana: $EVIL$")

    assert calls[1][1] == "memecoin_ANOTHER_20230102_0304.txt"
    assert calls[1][2].startswith("\U0001F525 New memecoin on Solana: $ANOTHER")


def test_generate_and_queue_chart(monkeypatch, tmp_path):
    class FakeCG:
        def get_coin_market_chart_by_id(self, coin_id, vs_currency="usd", days=1):
            assert coin_id == "bitcoin"
            return {"prices": [[1, 10], [2, 20]]}

    class FakePLT:
        def __init__(self):
            self.saved = None
        def figure(self, *a, **k):
            pass
        def plot(self, *a, **k):
            pass
        def title(self, *a, **k):
            pass
        def xlabel(self, *a, **k):
            pass
        def ylabel(self, *a, **k):
            pass
        def xticks(self, *a, **k):
            pass
        def tight_layout(self):
            pass
        def savefig(self, path):
            self.saved = path
        def close(self):
            pass

    fixed_dt = datetime(2023, 1, 2, 3, 4)
    class DummyDT(datetime):
        @classmethod
        def now(cls):
            return fixed_dt

    fake_plt = FakePLT()
    monkeypatch.setattr(generate_content, "CoinGeckoAPI", lambda: FakeCG())
    monkeypatch.setattr(generate_content, "plt", fake_plt)
    monkeypatch.setattr(generate_content, "get_output_base_folder", lambda: str(tmp_path))
    monkeypatch.setattr(generate_content, "get_bot_mode", lambda: "post")
    monkeypatch.setattr(generate_content, "has_telegram", lambda: False)
    monkeypatch.setattr(generate_content, "datetime", DummyDT)

    generate_content.generate_and_queue_chart("bot1")

    expected = tmp_path / "bot1" / "chart_20230102_0304.png"
    assert fake_plt.saved == str(expected)
    assert (tmp_path / "bot1").is_dir()

