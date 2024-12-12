from pyredis.protocol import parse_frame, SimpleString, BulkString, Error, Nil, Integer, Array
from pyredis.datastore import Data
import datetime

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
            case BulkString("LPUSH"):
                print("LPUSH command trigger")
                return lpush_command(value, datastore), size
            case BulkString("RPUSH"):
                return rpush_command(value, datastore), size
            case BulkString("LRANGE"):
                return lrange_command(value, datastore), size
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
        if len(input.data) < 3:
            return Error("ERR wrong number of arguments for 'set' command").serialize()

        key = input.data[1].data
        value = input.data[2].data
        expiry = None

        if len(input.data) > 3:
            try:
                arg_key = input.data[3].data
                if arg_key == "EX":
                    arg_value = int(input.data[4].data)
                    expiry = datetime.datetime.now() + datetime.timedelta(seconds=arg_value)
                elif arg_key == "PX":
                    arg_value = int(input.data[4].data)
                    expiry = datetime.datetime.now() + datetime.timedelta(milliseconds=arg_value)
                else:
                    return Error("ERR syntax error").serialize()
            except KeyError:
                return Error("ERR syntax error").serialize()

        stored_data = Data(value=value, expiry=expiry)
        datastore.set(key, stored_data)
        return SimpleString("OK").serialize()
    except Exception as e:
        return Error(e).serialize()


def get_command(input, datastore):
    try:
        if len(input.data) != 2:
            return Error("ERR wrong number of arguments for 'get' command").serialize()

        key = input.data[1].data
        stored_data = datastore.get(key)
        value = stored_data.value
        return BulkString(value).serialize()
    except Exception:
        return Nil().serialize()


def exist_command(input, datastore):
    try:
        if len(input.data) != 2:
            return Error("ERR wrong number of arguments for 'exist' command").serialize()
        key = input.data[1].data
        stored_data = datastore.get(key)
        if stored_data == "":
            return Integer(0).serialize()
        else:
            return Integer(1).serialize()
    except Exception as e:
        return Error(e).serialize()


def lpush_command(input, datastore):
    try:
        if len(input.data) < 2:
            return Error("ERR wrong number of arguments for 'lpush' command").serialize()

        key = input.data[1].data
        stored_data = datastore.get(key)
        elements = input.data[2:]

        if stored_data == "":
            datastore.set(key, Data(value=elements))
            stored_data = datastore.get(key)
        else:
            datastore.set(key, Data(value=elements + stored_data.value))

        new_len = len(datastore.get(key).value)
        return Integer(new_len).serialize()

    except Exception as e:
        return Error(e).serialize()


def rpush_command(input, datastore):
    try:
        if len(input.data) < 2:
            return Error("ERR wrong number of arguments for 'rpush' command").serialize()

        key = input.data[1].data
        stored_data = datastore.get(key)
        elements = input.data[2:]

        if stored_data == "":
            datastore.set(key, Data(value=elements))
            stored_data = datastore.get(key)
        else:
            datastore.set(key, Data(value=stored_data.value + elements))

        new_len = len(datastore.get(key).value)
        return Integer(new_len).serialize()

    except Exception as e:
        return Error(e).serialize()


def lrange_command(input, datastore):
    try:
        if len(input.data) != 4:
            return Error("ERR wrong number of arguments for 'lrange' command").serialize()

        key = input.data[1].data
        stored_data = datastore.get(key)
        start = int(input.data[2].data)
        end = int(input.data[3].data)

        if stored_data == "":
            print("empty array")
            return Array([]).serialize()
        else:
            elements = list(map(lambda x: BulkString(x), stored_data.value[start : end + 1]))

            return Array(elements).serialize()

    except Exception as e:
        return Error(e).serialize()
