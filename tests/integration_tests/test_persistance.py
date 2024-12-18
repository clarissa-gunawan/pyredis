import os
import subprocess
import time


def test_persistance():
    test_filepath = "tmp/test/persistance_test.aof"
    port = str(6381)

    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    assert not os.path.exists(test_filepath)

    redis_process = subprocess.Popen(
        ["python", "-m", "pyredis", "--port", port, "--persistance", "--persistor-filepath", test_filepath]
    )
    time.sleep(0.2)  # Allow some time for the server to start

    assert os.path.exists(test_filepath)

    res = subprocess.run(["redis-cli", "-p", port, "SET", "message_persistance", "Hello World"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "OK"

    res = subprocess.run(["redis-cli", "-p", port, "GET", "message_persistance"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "Hello World"

    redis_process.terminate()

    redis_process = subprocess.Popen(
        ["python", "-m", "pyredis", "--port", port, "--persistance", "--persistor-filepath", test_filepath]
    )
    time.sleep(0.2)  # Allow some time for the server to start

    res = subprocess.run(["redis-cli", "-p", port, "GET", "message_persistance"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "Hello World"

    redis_process.terminate()

    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    assert not os.path.exists(test_filepath)
