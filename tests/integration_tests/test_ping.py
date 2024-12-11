# TODO: The following runs into a warning: OSError: [Errno 48] Address already in use
import subprocess


def test_ping(server):
    res = subprocess.run(["redis-cli", "-p", "6380", "PING"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "PONG"


def test_ping_with_param(server):
    res = subprocess.run(["redis-cli", "-p", "6380", "PING", "HELLO"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "HELLO"
