'''

RESP (Redis Serialization Protocol)
Spec: https://redis.io/docs/latest/develop/reference/protocol-spec/

- For **Simple Strings** the first byte of the reply is "+"     "+OK\r\n"
- For **Errors** the first byte of the reply is "-"             "-Error message\r\n"
- For **Integers** the first byte of the reply is ":"           ":[<+|->]<value>\r\n"
- For **Bulk Strings** the first byte of the reply is "$"       "$<length>\r\n<data>\r\n"
- For **Arrays** the first byte of the reply is "``"            "*<number-of-elements>\r\n<element-1>...<element-n>"

We need a module that extracts messages from the stream.
When we read from the network we will get:
1. A partial message.
2. A whole message.
3. A whole message, followed by either 1 or 2
We will need to remove parsed bytes from the stream.
'''

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from pyredis.protocol import parse_frame, SimpleString

import pytest

@pytest.mark.parametrize("buffer, expected", [
    # Simple String
    (b"+OK", (None, 0)),
    (b"+OK\r\n", (SimpleString("OK"), 5)),
    (b"+OK\r\n+Partial", (SimpleString("OK"), 5)),
])
def test_parse_frame(buffer, expected):
    got = parse_frame(buffer)
    assert got[0] == expected[0]
    assert got[1] == expected[1]


if __name__ == "__main__":
    sys.exit(pytest.main())