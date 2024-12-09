from dataclasses import dataclass

@dataclass
class SimpleString():
    data: str

DELIMITER = b"\r\n"
DELIMITER_SIZE = 2

def parse_frame(buffer):
    end = buffer.find(DELIMITER)
    if end == -1:
        return None, 0

    match chr(buffer[0]):
        case "+":
            return SimpleString(buffer[1: end].decode('ascii')), end + DELIMITER_SIZE
    
    return None, 0
