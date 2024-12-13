"""

REDIS Commands

"""

import pytest
from pyredis.commands import parse_command
from pyredis.datastore import QueueDataStore, Data
from pyredis.protocol import BulkString


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
        (b"*5\r\n$3\r\nSET\r\n$7\r\nmessage\r\n$11\r\nHello World\r\n$2\r\nEX\r\n$1\r\n1\r\n", (b"+OK\r\n", 59)),
        (b"*5\r\n$3\r\nSET\r\n$7\r\nmessage\r\n$11\r\nHello World\r\n$2\r\nPX\r\n$3\r\n100\r\n", (b"+OK\r\n", 61)),
        # Get Command
        (b"*2\r\n$3\r\nGET\r\n$4\r\nkey1\r\n", (b"$6\r\nvalue1\r\n", 23)),
        (b"*2\r\n$3\r\nGET\r\n$4\r\nkey2\r\n", (b"$-1\r\n", 23)),
        (b"*3\r\n$3\r\nGET\r\n$7\r\nmessage\r\n$3\r\ntry\r\n", (b"-ERR wrong number of arguments for 'get' command\r\n", 35)),
        # Exists Command
        (b"*2\r\n$6\r\nEXISTS\r\n$4\r\nkey1\r\n", (b":1\r\n", 26)),
        (b"*2\r\n$6\r\nEXISTS\r\n$4\r\nkey2\r\n", (b":0\r\n", 26)),
        (
            b"*3\r\n$6\r\nEXISTS\r\n$7\r\nmessage\r\n$3\r\ntry\r\n",
            (b"-ERR wrong number of arguments for 'exists' command\r\n", 38),
        ),
        # LPush Command
        (b"*3\r\n$5\r\nLPUSH\r\n$8\r\nlps_list\r\n$16\r\nHello World Left\r\n", (b":1\r\n", 52)),
        (b"*3\r\n$5\r\nLPUSH\r\n$5\r\nlist1\r\n$10\r\nlistvalue11\r\n", (b":2\r\n", 43)),
        # RPush Command
        (b"*3\r\n$5\r\nRPUSH\r\n$8\r\nrps_list\r\n$17\r\nHello World Right\r\n", (b":1\r\n", 53)),
        (b"*3\r\n$5\r\nRPUSH\r\n$5\r\nlist1\r\n$10\r\nlistvalue22\r\n", (b":2\r\n", 43)),
        # LRange Command
        (b"*4\r\n$6\r\nLRANGE\r\n$8\r\nlrg_list\r\n$1\r\n0\r\n$1\r\n1\r\n", (b"*0\r\n", 44)),
        (
            b"*4\r\n$6\r\nLRANGE\r\n$5\r\nlist3\r\n$1\r\n0\r\n$1\r\n1\r\n",
            (b"*2\r\n$10\r\nlistvalue3\r\n$11\r\nlistvalue33\r\n", 41),
        ),
        (
            b"*4\r\n$6\r\nLRANGE\r\n$5\r\nlist3\r\n$4\r\n-100\r\n$3\r\n100\r\n",
            (b"*3\r\n$10\r\nlistvalue3\r\n$11\r\nlistvalue33\r\n$12\r\nlistvalue333\r\n", 46),
        ),
    ],
)
def test_parse_command(buffer, expected):
    datastore = QueueDataStore()
    datastore.set("key1", Data(value="value1"))
    datastore.set("list1", Data(value=[BulkString("listvalue1")]))
    datastore.set("list2", Data(value=[BulkString("listvalue2")]))
    datastore.set(
        "list3", Data(value=[BulkString(data="listvalue3"), BulkString(data="listvalue33"), BulkString(data="listvalue333")])
    )
    got = parse_command(buffer, datastore)
    assert got == expected
