import time
import threading

import pytest

import pyredis

@pytest.fixture
def server(scope="module"):
    threading.Thread(target=pyredis.main, daemon=True).start()
    time.sleep(0.1) # 100ms
    yield