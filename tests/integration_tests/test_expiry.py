import subprocess
import time


def test_set_get_before_expiry_seconds(async_server):
    res = subprocess.run(
        ["redis-cli", "-p", "6380", "SET", "msg_sec_before_expiry", "Hello World", "EX", "1"], stdout=subprocess.PIPE
    )
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "OK"
    res = subprocess.run(["redis-cli", "-p", "6380", "GET", "msg_sec_before_expiry"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "Hello World"


def test_set_get_after_expiry_seconds(async_server):
    res = subprocess.run(
        ["redis-cli", "-p", "6380", "SET", "msg_sec_after_expiry", "Hello World", "EX", "1"], stdout=subprocess.PIPE
    )
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "OK"
    time.sleep(1)  # 1s
    res = subprocess.run(["redis-cli", "-p", "6380", "GET", "msg_sec_after_expiry"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == ""


def test_set_get_before_expiry_miliseconds(async_server):
    res = subprocess.run(
        ["redis-cli", "-p", "6380", "SET", "msg_ms_before_expiry", "Hello World", "PX", "100"], stdout=subprocess.PIPE
    )
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "OK"
    res = subprocess.run(["redis-cli", "-p", "6380", "GET", "msg_ms_before_expiry"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "Hello World"


def test_set_get_after_expiry_miliseconds(async_server):
    res = subprocess.run(
        ["redis-cli", "-p", "6380", "SET", "msg_ms_after_expiry", "Hello World", "PX", "100"], stdout=subprocess.PIPE
    )
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == "OK"
    time.sleep(0.1)  # 200ms
    res = subprocess.run(["redis-cli", "-p", "6380", "GET", "msg_ms_after_expiry"], stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert res.stdout.decode("utf-8").strip() == ""
