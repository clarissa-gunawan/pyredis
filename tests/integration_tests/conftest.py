import time
import threading

from pyredis.datastore.lock_datastore import LockDataStore
import pytest

import pyredis

def setup_datastore():
    ds = LockDataStore()
    ds["test_key"] = "test_value"
    return ds


@pytest.fixture(scope="session")
def async_server():
    threading.Thread(target=pyredis.main, kwargs={"threaded": False, "datastore": setup_datastore()}, daemon=True).start()
    time.sleep(0.1)  # 100ms
    yield

# TODO: Blocked by  OSError: [Errno 48] Address already in use
# when running with the async server
# @pytest.fixture(scope="session")
# def threaded_server():
#     threading.Thread(target=pyredis.main, kwargs={"threaded": True, "datastore": setup_datastore()}, daemon=True).start()
#     time.sleep(0.1)  # 100ms
#     yield
