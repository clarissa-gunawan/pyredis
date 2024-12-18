import time
import pytest
import subprocess


@pytest.fixture(scope="session")
def async_server():
    # Start the Redis server
    redis_process = subprocess.Popen(["python", "-m", "pyredis"])
    time.sleep(0.5)  # Allow some time for the server to start
    yield
    redis_process.terminate()
