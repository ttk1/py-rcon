import re

FORMATTING_CODE_PATTERN = re.compile(r'§[0-9a-z]')


def int_to_bytes(value):
    return value.to_bytes(4, byteorder='little')


def bytes_to_int(value):
    return int.from_bytes(value, byteorder='little')


def remove_formatting_codes(text):
    return FORMATTING_CODE_PATTERN.sub('', text)
