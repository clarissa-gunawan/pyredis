import subprocess


def test_lrange(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "LPUSH", "msg_lrange", "first_msg", "second_msg"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "2"
    res = subprocess.run(["redis-cli", "-p", "6380", "RPUSH", "msg_lrange", "third_msg"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "3"

    res = subprocess.run(["redis-cli", "-p", "6380", "LRANGE", "msg_lrange", "0", "1"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "second_msg\nfirst_msg"

    res = subprocess.run(["redis-cli", "-p", "6380", "LRANGE", "msg_lrange", "-100", "100"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "second_msg\nfirst_msg\nthird_msg"


def test_lrange_no_data(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "LRANGE", "msg_lrange_no_data", "0", "1"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == ""


def test_lrange_missing_argument(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "LRANGE"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "ERR wrong number of arguments for 'lrange' command"
