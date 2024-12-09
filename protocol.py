
def parse_frame(buffer):
    
    match chr(buffer[0]):
        case "+":
            return "OK", 5
    
    return None, 0
