import os
import sys
import types

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Stub logger
logger_mod = types.ModuleType("logger")
logger_mod.logger = types.SimpleNamespace(info=lambda *a, **k: None,
                                          warning=lambda *a, **k: None,
                                          error=lambda *a, **k: None)
sys.modules.setdefault("utils.logger", logger_mod)

# Stub requests module so import works even if not installed
requests_mod = types.ModuleType("requests")
requests_mod.get = lambda *a, **k: None
sys.modules.setdefault("requests", requests_mod)

sys.modules.pop("reputation_checker", None)
import reputation_checker


def test_is_token_valid_skips_non_eth(monkeypatch):
    called = []
    monkeypatch.setattr(reputation_checker, "get_deployer_reputation",
                        lambda addr: called.append(addr) or 10)

    token = {"chain": "solana", "deployer": "0xD"}
    assert reputation_checker.is_token_valid(token, min_reputation_score=5)
    assert called == []


def test_is_token_valid_checks_eth(monkeypatch):
    called = []

    def fake_rep(addr):
        called.append(addr)
        return 6

    monkeypatch.setattr(reputation_checker, "get_deployer_reputation", fake_rep)

    token = {"chain": "Ethereum", "deployer": "0xA"}
    assert reputation_checker.is_token_valid(token, min_reputation_score=5)
    assert called == ["0xA"]
