import hashlib
def from_hex_string(hex_string):
    # Ensure the length of the hexadecimal string is even
    if len(hex_string) % 2 != 0:
        raise ValueError("Hexadecimal string must have an even length")

    # Convert pairs of characters to bytes
    bytes_list = [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]

    # Convert the list of integers to bytes
    result_bytes = bytes(bytes_list)
    
    return result_bytes

pin_bytes_true = from_hex_string("d04988522ddfed3133cc24fb6924eae9")

#brute_force
for pin in range(1000000):
    pin = str(pin).zfill(6)
    print(pin)
    pin_bytes = pin.encode('utf-8')
    for i in range(25):
        for j in range(400):
            md = hashlib.md5()
            md.update(pin_bytes)
            pin_bytes = md.digest()
        
    if pin_bytes == pin_bytes_true:
        print("ENCONTRADOOO")
        print(pin)
        break