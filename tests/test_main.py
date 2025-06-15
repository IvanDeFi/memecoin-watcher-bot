import os
import sys
import types
import json

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Stub dependencies for main import
logger_mod = types.ModuleType("logger")
logger_mod.logger = types.SimpleNamespace(info=lambda *a, **k: None,
                                          warning=lambda *a, **k: None,
                                          error=lambda *a, **k: None)
sys.modules.setdefault("utils.logger", logger_mod)

dotenv_mod = types.ModuleType("dotenv")
dotenv_mod.load_dotenv = lambda: None
sys.modules.setdefault("dotenv", dotenv_mod)

settings_mod = types.ModuleType("utils.settings")
settings_mod.get_config = lambda: {}
sys.modules.setdefault("utils.settings", settings_mod)

gc_mod = types.ModuleType("generate_content")
gc_mod.generate_and_queue_chart = lambda *a, **k: None
gc_mod.generate_and_queue_exchange_info = lambda *a, **k: None
gc_mod.generate_and_queue_memecoin_tweet = lambda *a, **k: None
gc_mod.generate_and_queue_comment = lambda *a, **k: None
sys.modules.setdefault("generate_content", gc_mod)

import main


def test_get_next_content_type_updates_state(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cycle = ["a", "b", "c"]

    first = main.get_next_content_type(cycle)
    assert first == "a"
    assert json.loads(open("state.json", encoding="utf-8").read()) == {"index": 1}

    second = main.get_next_content_type(cycle)
    assert second == "b"
    assert json.loads(open("state.json", encoding="utf-8").read()) == {"index": 2}

    third = main.get_next_content_type(cycle)
    assert third == "c"
    assert json.loads(open("state.json", encoding="utf-8").read()) == {"index": 0}
