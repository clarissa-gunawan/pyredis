import time
import threading

import pytest

import pyredis


@pytest.fixture(scope="session")
def async_server():
    threading.Thread(target=pyredis.main, kwargs={"threaded": False}, daemon=True).start()
    time.sleep(0.1)  # 100ms
    yield


@pytest.fixture(scope="session")
def threaded_server():
    threading.Thread(target=pyredis.main, kwargs={"port": 6382, "threaded": True}, daemon=True).start()
    time.sleep(0.1)  # 100ms
    yield
