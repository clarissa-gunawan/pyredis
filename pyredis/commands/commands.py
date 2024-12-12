from pyredis.protocol import parse_frame, SimpleString, BulkString, Error, Nil

"""
Redis generally uses RESP as a request-response protocol in the following way:

Clients send commands to a Redis server as an array of bulk strings. The first (and 
sometimes also the second) bulk string in the array is the command's name. Subsequent 
elements of the array are the arguments for the command.
The server replies with a RESP type. The reply's type is determined by the command's 
implementation and possibly by the client's protocol version.
"""


def parse_command(buffer, datastore=None):
    print(f"BUFFER: {buffer}")
    value, size = parse_frame(buffer)
    print(f"PARSED BUFFER: {value}")
    if value is None:
        return None, 0

    try:
        match value.data[0]:
            case BulkString("PING"):
                return ping_command(value), size
            case BulkString("ECHO"):
                return echo_command(value), size
            case BulkString("SET"):
                return set_command(value, datastore), size
            case BulkString("GET"):
                return get_command(value, datastore), size
            case _:
                return Error("Error: Not a valid command").serialize(), size
    except Exception as e:
        return Error(e).serialize(), size


def ping_command(input):
    try:
        if len(input.data) > 1:
            return input.data[1].serialize()
    except Exception as e:
        return Error(e).serialize()

    return SimpleString("PONG").serialize()


def echo_command(input):
    try:
        if len(input.data) > 1:
            return input.data[1].serialize()
    except Exception as e:
        return Error(e).serialize()
    return BulkString("").serialize()


def set_command(input, datastore):
    try:
        if len(input.data) != 3:
            return Error("ERR wrong number of arguments for 'set' command").serialize()

        key = input.data[1].data
        value = input.data[2].data
        datastore.set(key, value)
        return SimpleString("OK").serialize()
    except Exception as e:
        return Error(e).serialize()


def get_command(input, datastore):
    try:
        if len(input.data) != 2:
            return Error("ERR wrong number of arguments for 'get' command").serialize()

        key = input.data[1].data
        value = datastore.get(key)
        return BulkString(value).serialize()
    except Exception:
        return Nil().serialize()
