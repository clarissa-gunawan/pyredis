"""

REDIS Commands

"""


import pytest
from pyredis.commands import ping_command, echo_command


@pytest.mark.parametrize(
        "buffer, expected",
        [
            (b"", b"PONG"),
            (b"Hello World", b"Hello World"),
        ]
)
def test_ping_command(buffer, expected):
    got = ping_command(buffer)
    assert got == expected


@pytest.mark.parametrize(
        "buffer, expected",
        [
            (b"Hello World", b"Hello World"),
        ]
)
def test_echo_command(buffer, expected):
    got = echo_command(buffer)
    assert got == expected
