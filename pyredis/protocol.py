from dataclasses import dataclass
from typing import List

@dataclass
class SimpleString:
    data: str

@dataclass
class Error:
    message: str

@dataclass
class Integer:
    data: int

@dataclass
class BulkString:
    data: str

@dataclass
class Array:
    data: List

DELIMITER = b"\r\n"
DELIMITER_SIZE = 2

def parse_frame(buffer):
    end = buffer.find(DELIMITER)
    if end == -1:
        return None, 0

    match chr(buffer[0]):
        case "+":
            return SimpleString(buffer[1: end].decode('ascii')), end + DELIMITER_SIZE
        
        case "-":
            return Error(buffer[1: end].decode('ascii')), end + DELIMITER_SIZE
        
        case ":":
            return Integer(int(buffer[1: end].decode('ascii'))), end + DELIMITER_SIZE
        
        case "$":
            expected_length = int(buffer[1: end].decode('ascii'))
            size = end + DELIMITER_SIZE + expected_length + DELIMITER_SIZE

            if len(buffer) >= size:
                value = buffer[end + DELIMITER_SIZE: end + DELIMITER_SIZE + expected_length].decode('ascii')
                return BulkString(value), size
            
        case "*":
            expected_count = int(buffer[1: end].decode('ascii'))
            actual_count = buffer[end + DELIMITER_SIZE:].count(DELIMITER)

            if actual_count >= expected_count:
                current_arr = []
                current_size = end + DELIMITER_SIZE
                for _ in range(expected_count):
                    new_input = buffer[current_size:]
                    value, size = parse_frame(new_input)
                    if size == 0:
                        return None, 0
                    current_arr.append(value)
                    current_size += size

                return Array(current_arr), current_size              
    
    return None, 0
