import time

from pyredis.datastore import QueueDataStore, Data

import pytest

import subprocess


def setup_datastore():
    ds = QueueDataStore()
    ds.set("test_key", Data(value="test_value"))
    return ds


@pytest.fixture(scope="session")
def async_server():
    # Start the Redis server
    redis_process = subprocess.Popen(["python", "-m", "pyredis"])
    time.sleep(0.2)  # Allow some time for the server to start
    yield
    redis_process.terminate()
