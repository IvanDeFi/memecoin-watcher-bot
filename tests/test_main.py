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

# Stub filelock to avoid external dependency
filelock_mod = types.ModuleType("filelock")

import threading


class DummyLock:
    _locks = {}

    def __init__(self, path):
        # create the lock file if it doesn't exist
        open(path, "a").close()
        self._lock = DummyLock._locks.setdefault(path, threading.Lock())

    def __enter__(self):
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._lock.release()

filelock_mod.FileLock = DummyLock
sys.modules.setdefault("filelock", filelock_mod)

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


def test_get_next_content_type_waits_for_lock(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cycle = ["a", "b"]
    lock_path = main.STATE_FILE + ".lock"

    # Acquire the lock in the main thread
    lock = main.filelock.FileLock(lock_path)
    start = threading.Event()
    finish = threading.Event()

    def run():
        start.set()
        main.get_next_content_type(cycle)
        finish.set()

    with lock:
        t = threading.Thread(target=run)
        t.start()
        start.wait()
        assert not finish.is_set()
    t.join(timeout=1)
    assert finish.is_set()
