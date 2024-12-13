import subprocess


def test_exists_exists(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "EXISTS", "test_key"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "1"


def test_exists_does_not_exists(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "EXISTS", "unknown_key"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "0"


def test_exists_missing_argument(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "EXISTS"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "ERR wrong number of arguments for 'exists' command"
