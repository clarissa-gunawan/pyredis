"""

RESP (Redis Serialization Protocol)
Spec: https://redis.io/docs/latest/develop/reference/protocol-spec/

- For **Simple Strings** the first byte of the reply is "+"     "+OK\r\n"
- For **Errors** the first byte of the reply is "-"             "-Error message\r\n"
- For **Integers** the first byte of the reply is ":"           ":[<+|->]<value>\r\n"
- For **Bulk Strings** the first byte of the reply is "$"       "$<length>\r\n<data>\r\n"
- For **Arrays** the first byte of the reply is "*"            "*<number-of-elements>\r\n<element-1>...<element-n>"

We need a module that extracts messages from the stream.
When we read from the network we will get:
1. A partial message.
2. A whole message.
3. A whole message, followed by either 1 or 2
We will need to remove parsed bytes from the stream.
"""

from pyredis.protocol import (
    parse_frame,
    SimpleString,
    Error,
    Integer,
    BulkString,
    Array,
    Null,
)

import pytest


@pytest.mark.parametrize(
    "buffer, expected",
    [
        # Simple String
        (b"+OK", (None, 0)),
        (b"+OK\r\n", (SimpleString("OK"), 5)),
        (b"+OK\r\n+Partial", (SimpleString("OK"), 5)),
        (b"+OK\r\n+Second Message\r\n", (SimpleString("OK"), 5)),
        # Error
        (b"-Err", (None, 0)),
        (b"-Error Message\r\n", (Error("Error Message"), 16)),
        (b"-Error Message\r\n+Partial", (Error("Error Message"), 16)),
        # Integer
        (b":1", (None, 0)),
        (b":100\r\n", (Integer(100), 6)),
        (b":100\r\n:200", (Integer(100), 6)),
        # Bulk String
        (b"$0\r\n\r\n", (BulkString(""), 6)),
        (b"$8\r\nPartial", (None, 0)),
        (b"$11\r\nBulk String\r\n", (BulkString("Bulk String"), 18)),
        (b"$8\r\nBulk Str\r\n+OK", (BulkString("Bulk Str"), 14)),
        # Array
        (b"*", (None, 0)),
        (b"*0\r\n", (Array([]), 0)),
        # Array with Simple String
        (b"*1\r\n+OK", (None, 0)),
        (b"*1\r\n+OK\r\n", (Array([SimpleString("OK")]), 9)),
        (
            b"*2\r\n+Hello\r\n+World\r\n",
            (Array([SimpleString("Hello"), SimpleString("World")]), 20),
        ),
        (
            b"*2\r\n+Hello\r\n+World\r\n:Test",
            (Array([SimpleString("Hello"), SimpleString("World")]), 20),
        ),
        # Array with Error
        (b"*1\r\n-Err", (None, 0)),
        (b"*1\r\n-Error Message 1\r\n", (Array([Error("Error Message 1")]), 22)),
        (
            b"*2\r\n-Error Message 1\r\n-Error Message 2\r\n",
            (Array([Error("Error Message 1"), Error("Error Message 2")]), 40),
        ),
        (
            b"*2\r\n-Error Message 1\r\n-Error Message 2\r\n-Err",
            (Array([Error("Error Message 1"), Error("Error Message 2")]), 40),
        ),
        # Array with Integers
        (b"*1\r\n:10", (None, 0)),
        (b"*1\r\n:300\r\n", (Array([Integer(300)]), 10)),
        (b"*2\r\n:300\r\n:400\r\n", (Array([Integer(300), Integer(400)]), 16)),
        (b"*2\r\n:300\r\n:400\r\n:50", (Array([Integer(300), Integer(400)]), 16)),
        # Array with Bulk String
        (b"*1\r\n$8\r\nPartial", (None, 0)),
        (b"*1\r\n$11\r\nBulk String\r\n", (Array([BulkString("Bulk String")]), 22)),
        (
            b"*2\r\n$11\r\nBulk String\r\n$11\r\nHello World\r\n",
            (Array([BulkString("Bulk String"), BulkString("Hello World")]), 40),
        ),
        (
            b"*2\r\n$11\r\nBulk String\r\n$11\r\nHello World\r\n*1",
            (Array([BulkString("Bulk String"), BulkString("Hello World")]), 40),
        ),
    ],
)
def test_parse_frame(buffer, expected):
    got = parse_frame(buffer)
    assert got[0] == expected[0]
    assert got[1] == expected[1]


@pytest.mark.parametrize(
    "input, expected",
    [
        (SimpleString("OK"), b"+OK\r\n"),
        (Error("Error Message"), b"-Error Message\r\n"),
        (Integer(100), b":100\r\n"),
        (BulkString("Bulk String"), b"$11\r\nBulk String\r\n"),
        (BulkString(None), b"$-1\r\n"),
        (BulkString(""), b"$0\r\n\r\n"),
        (Array([]), b"*0\r\n"),
        (Array(None), b"*-1\r\n"),
        (Array([Integer(1), Integer(2)]), b"*2\r\n:1\r\n:2\r\n"),
        (Null(), b"_\r\n"),
    ],
)
def test_serialize(input, expected):
    got = input.serialize()
    assert got == expected
