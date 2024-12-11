"""

REDIS Commands

"""

import pytest
from pyredis.commands import parse_command


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
    ],
)
def test_parse_command(buffer, expected):
    got = parse_command(buffer)
    assert got == expected
