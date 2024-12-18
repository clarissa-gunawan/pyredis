import subprocess


def test_get(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "SET", "test_key", "test_value"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "OK"

    res = subprocess.run(["redis-cli", "-p", "6380", "GET", "test_key"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "test_value"


def test_get_with_unknown_key(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "GET", "unknown_key"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == ""


def test_get_missing_argument(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "GET", "message", "key"], stdout=subprocess.PIPE)
    assert res.stdout.decode("utf-8").strip() == "ERR wrong number of arguments for 'get' command"
