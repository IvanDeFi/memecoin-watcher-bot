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
sys.modules.setdefault("matplotlib", matplotlib)
sys.modules.setdefault("matplotlib.pyplot", plt)

# Stub internal modules that rely on external services
fetcher = types.ModuleType("token_fetcher")
fetcher.fetch_new_tokens = lambda chain: []
sys.modules["parser.token_fetcher"] = fetcher

reputation = types.ModuleType("reputation_checker")
reputation.is_token_valid = lambda token: True
sys.modules["reputation_checker"] = reputation

poster_mod = types.ModuleType("poster")
poster_mod.queue_for_zenno = lambda *a, **k: None
sys.modules["poster"] = poster_mod

logger_mod = types.ModuleType("logger")
logger_mod.logger = types.SimpleNamespace(info=lambda *a, **k: None,
                                          warning=lambda *a, **k: None,
                                          error=lambda *a, **k: None)
sys.modules["utils.logger"] = logger_mod

from generate_content import sanitize_filename_component


def test_sanitize_filename_component():
    text = "token name$%_.123"
    result = sanitize_filename_component(text)
    assert result == "tokenname_123"
