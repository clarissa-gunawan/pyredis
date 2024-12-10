"""

REDIS Commands

"""


import pytest
from pyredis.commands import parse_command


@pytest.mark.parametrize(
        "buffer, expected",
        [
            # Ping Command
            (b"*1\r\n+PING\r\n", b"*1\r\n+PONG\r\n"),
            (b"*2\r\n+PING\r\n$11\r\nHello World\r\n", b"*1\r\n$11\r\nHello World\r\n"),
            # Echo Command
            (b"*1\r\n+ECHO\r\n", b"*0\r\n"),
            (b"*2\r\n+ECHO\r\n$11\r\nHello World\r\n", b"*1\r\n$11\r\nHello World\r\n"),
        ]
)
def test_parse_command(buffer, expected):
    got = parse_command(buffer)
    assert got == expected
