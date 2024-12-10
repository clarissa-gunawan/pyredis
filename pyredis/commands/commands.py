from pyredis.protocol import parse_frame, SimpleString, Array


def parse_command(buffer):
    value, _ = parse_frame(buffer)
    print(value)

    match value.data[0]:
        case SimpleString("PING"):
            return ping_command(value)
        case SimpleString("ECHO"):
            return echo_command(value)

    return None, 0
        

def ping_command(input):
    if len(input.data) > 1:
        input.data.pop(0)
        return input.serialize()

    return Array([SimpleString("PONG")]).serialize()

def echo_command(input):
    if len(input.data) > 1:
        input.data.pop(0)
        return input.serialize()
    
    return Array([]).serialize()