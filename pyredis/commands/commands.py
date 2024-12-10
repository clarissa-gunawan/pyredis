


def ping_command(buffer):
    if buffer:
        return buffer

    return b"PONG"

def echo_command(buffer):
    if buffer:
        return buffer
    
    return b""