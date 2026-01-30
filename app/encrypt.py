import hashlib
def anyfunname(pin):
    new_pin = hashlib.sha512(str(pin).encode()).hexdigest()
    return new_pin