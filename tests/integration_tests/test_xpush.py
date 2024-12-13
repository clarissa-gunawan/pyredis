import subprocess


def test_lpush(async_server):
    res = subprocess.run(
        ["redis-cli", "-p", "6380", "LPUSH", "message_lpush", "first_msg", "second_msg"], stdout=subprocess.PIPE
    )
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "2"


def test_lpush_missing_argument(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "LPUSH"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "ERR wrong number of arguments for 'lpush' command"


def test_rpush(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "RPUSH", "message_rpush", "first_msg"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "1"


def test_rpush_missing_argument(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "RPUSH"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "ERR wrong number of arguments for 'rpush' command"
