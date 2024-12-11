import time
import threading

import pytest

import pyredis


@pytest.fixture
def async_server(scope="module"):
    threading.Thread(target=pyredis.main, kwargs={"threaded": False}, daemon=True).start()
    time.sleep(0.1)  # 100ms
    yield

@pytest.fixture
def threaded_server(scope="module"):
    threading.Thread(target=pyredis.main, kwargs={"threaded": True}, daemon=True).start()
    time.sleep(0.1)  # 100ms
    yield