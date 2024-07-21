import hashlib

class PinChecker:
    def __init__(self):
        pass

    @staticmethod
    def check_pin(pin):
        if len(pin) != 6:
            return False

        try:
            pin_bytes = pin.encode('utf-8')

            for i in range(25):
                for j in range(400):
                    md = hashlib.md5()
                    md.update(pin_bytes)
                    pin_bytes = md.digest()

            hex_pin_bytes = PinChecker.to_hex_string(pin_bytes)
            return hex_pin_bytes == "d04988522ddfed3133cc24fb6924eae9"

        except Exception as e:
            print(f"Exception while checking pin: {e}")
            return False

    @staticmethod
    def to_hex_string(bytes):
        hex_string = ''.join([format(b, '02x') for b in bytes])
        return hex_string


# Example usage:
pin_to_check = "123456"
result = PinChecker.check_pin(pin_to_check)
print(result)
