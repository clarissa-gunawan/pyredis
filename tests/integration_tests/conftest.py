import time
import threading

from pyredis.datastore.lock_datastore import LockDataStore
import pytest

import pyredis


@pytest.fixture(scope="session")
def async_server():
    ds = LockDataStore()
    ds["test_key"] = "test_value"
    threading.Thread(target=pyredis.main, kwargs={"threaded": False, "datastore": ds}, daemon=True).start()
    time.sleep(0.1)  # 100ms
    yield


@pytest.fixture(scope="session")
def threaded_server():
    threading.Thread(target=pyredis.main, kwargs={"port": 6382, "threaded": True}, daemon=True).start()
    time.sleep(0.1)  # 100ms
    yield
