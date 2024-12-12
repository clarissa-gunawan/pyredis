"""

REDIS Commands

"""

import pytest
from pyredis.commands import parse_command
from pyredis.datastore.lock_datastore import LockDataStore


@pytest.mark.parametrize(
    "buffer, expected",
    [
        # Ping Command
        (b"*1\r\n$4\r\nPING\r\n", (b"+PONG\r\n", 14)),
        (
            b"*2\r\n$4\r\nPING\r\n$11\r\nHello World\r\n",
            (b"$11\r\nHello World\r\n", 32),
        ),
        # Echo Command
        (b"*1\r\n$4\r\nECHO\r\n", (b"$0\r\n\r\n", 14)),
        (
            b"*2\r\n$4\r\nECHO\r\n$11\r\nHello World\r\n",
            (b"$11\r\nHello World\r\n", 32),
        ),
        # Set Command
        (b"*3\r\n$3\r\nSET\r\n$7\r\nmessage\r\n$11\r\nHello World\r\n", (b"+OK\r\n", 44)),
        (b"*2\r\n$3\r\nSET\r\n$7\r\nmessage\r\n", (b"-ERR wrong number of arguments for 'set' command\r\n", 26)),
        # Get Command
        (b"*2\r\n$3\r\nGET\r\n$4\r\nkey1\r\n", (b"$6\r\nvalue1\r\n", 23)),
        (b"*2\r\n$3\r\nGET\r\n$4\r\nkey2\r\n", (b"$-1\r\n", 23)),
        (b"*3\r\n$3\r\nGET\r\n$7\r\nmessage\r\n$3\r\ntry\r\n", (b"-ERR wrong number of arguments for 'get' command\r\n", 35)),
    ],
)
def test_parse_command(buffer, expected):
    datastore = LockDataStore()
    datastore["key1"] = "value1"
    got = parse_command(buffer, datastore)
    assert got == expected
