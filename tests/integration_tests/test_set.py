import subprocess


def test_set(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "SET", "message_set", "Hello World"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "OK"


def test_set_missing_argument(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "SET", "message_set"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "ERR wrong number of arguments for 'set' command"
