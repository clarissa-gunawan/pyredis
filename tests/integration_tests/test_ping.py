import subprocess


def test_ping(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "PING"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "PONG"


def test_ping_with_param(async_server):
    res = subprocess.run(["redis-cli", "-p", "6380", "PING", "HELLO"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "HELLO"
