import os
import sys
import types
import pytest

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Stub logger and dotenv so scheduler imports
logger_mod = types.ModuleType("logger")
logger_mod.logger = types.SimpleNamespace(info=lambda *a, **k: None,
                                          error=lambda *a, **k: None)
sys.modules.setdefault("utils.logger", logger_mod)

dotenv_mod = types.ModuleType("dotenv")
dotenv_mod.load_dotenv = lambda: None
sys.modules.setdefault("dotenv", dotenv_mod)

# Stub schedule module so import succeeds
schedule_stub = types.ModuleType("schedule")
schedule_stub.every = lambda *a, **k: None
schedule_stub.run_pending = lambda: None
sys.modules.setdefault("schedule", schedule_stub)

# Stub modules used indirectly via main/generate_content
sys.modules.setdefault("pycoingecko", types.ModuleType("pycoingecko"))
sys.modules["pycoingecko"].CoinGeckoAPI = object

matplotlib = types.ModuleType("matplotlib")
plt = types.ModuleType("pyplot")
setattr(matplotlib, "pyplot", plt)
sys.modules.setdefault("matplotlib", matplotlib)
sys.modules.setdefault("matplotlib.pyplot", plt)

yaml_mod = types.ModuleType("yaml")
yaml_mod.safe_load = lambda s: {}
sys.modules.setdefault("yaml", yaml_mod)

requests_mod = types.ModuleType("requests")
requests_mod.get = lambda *a, **k: None
sys.modules.setdefault("requests", requests_mod)

reputation_mod = types.ModuleType("reputation_checker")
reputation_mod.is_token_valid = lambda token, min_score=None: True
sys.modules.setdefault("reputation_checker", reputation_mod)

poster_mod = types.ModuleType("poster")
poster_mod.queue_for_zenno = lambda *a, **k: None
sys.modules.setdefault("poster", poster_mod)

telegram_mod = types.ModuleType("telegram_bot")
telegram_mod.notify_pending = lambda *a, **k: None
sys.modules.setdefault("telegram_bot", telegram_mod)

import scheduler


def test_run_scheduler_one_cycle(monkeypatch):
    calls = {"main": 0}

    def fake_main():
        calls["main"] += 1

    jobs = []

    class FakeJob:
        def __init__(self, interval):
            self.interval = interval
        @property
        def seconds(self):
            return self
        def do(self, func):
            self.func = func
            jobs.append(self)
            return self

    def fake_every(interval):
        return FakeJob(interval)

    def fake_run_pending():
        for job in list(jobs):
            if hasattr(job, "func"):
                job.func()
        raise StopIteration()

    fake_schedule = types.SimpleNamespace(every=fake_every, run_pending=fake_run_pending)

    monkeypatch.setattr(scheduler, "schedule", fake_schedule)
    monkeypatch.setattr(scheduler, "main", fake_main)
    monkeypatch.setattr(scheduler, "get_interval_from_config", lambda: 2)
    monkeypatch.setattr(scheduler, "time", types.SimpleNamespace(sleep=lambda _s: None))

    with pytest.raises(StopIteration):
        scheduler.run_scheduler()

    assert calls["main"] == 1
    assert jobs and jobs[0].interval == 2
