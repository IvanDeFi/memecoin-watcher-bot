import os
import sys
import types

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Stub logger to avoid file writes during import
logger_mod = types.ModuleType("logger")
logger_mod.logger = types.SimpleNamespace(info=lambda *a, **k: None, error=lambda *a, **k: None)
sys.modules.setdefault("utils.logger", logger_mod)

# Stub requests so parser.token_fetcher imports without the real library
requests_mod = types.ModuleType("requests")
requests_mod.get = lambda *a, **k: None
sys.modules.setdefault("requests", requests_mod)

# Ensure the real module is imported
sys.modules.pop("parser.token_fetcher", None)

from parser import token_fetcher
from parser.token_fetcher import fetch_new_tokens


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload

    def raise_for_status(self):
        pass


def test_fetch_new_tokens_parses(monkeypatch):
    payload = {
        "data": [
            {
                "symbol": "AAA",
                "liquidity": 1000,
                "volume_30m": 500,
                "age_minutes": 12,
                "address": "0x1",
                "deployer": "0xD1",
            }
        ]
    }

    def fake_get(url, params=None, timeout=10):
        return DummyResponse(payload)

    monkeypatch.setattr(token_fetcher.requests, "get", fake_get)
    tokens = fetch_new_tokens("solana")

    assert tokens == [
        {
            "ticker": "AAA",
            "liquidity": 1000,
            "volume_30m": 500,
            "age_minutes": 12,
            "contract_address": "0x1",
            "deployer": "0xD1",
            "chain": "solana",
        }
    ]


def test_fetch_new_tokens_error(monkeypatch):
    def fake_get(*_a, **_k):
        raise Exception("boom")

    monkeypatch.setattr(token_fetcher.requests, "get", fake_get)
    tokens = fetch_new_tokens("ethereum")
    assert tokens == []

