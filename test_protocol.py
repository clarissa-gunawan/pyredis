
from protocol import parse_frame

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

def test_parse_frame():
    buffer = b"+OK"
    msg, size = parse_frame(buffer)
    assert msg == None
    assert size == 0


def test_parse_frame_full():
    buffer = b"+OK\r\n"
    msg, size = parse_frame(buffer)
    assert msg == "OK"
    assert size == 5


test_parse_frame()
test_parse_frame_full()