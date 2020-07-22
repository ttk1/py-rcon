def int_to_bytes(value):
    return value.to_bytes(4, byteorder='little')


def bytes_to_int(value):
    return int.from_bytes(value, byteorder='little')
