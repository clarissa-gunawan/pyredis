from dataclasses import dataclass

@dataclass
class SimpleString():
    data: str


def parse_frame(buffer):
    end = buffer.find(b"\r\n")
    if end == -1:
        return None, 0

    match chr(buffer[0]):
        case "+":
            return SimpleString(buffer[1: end].decode('ascii')), 5
    
    return None, 0
