from enum import Enum

from rcon.util import int_to_bytes, bytes_to_int


class PacketType(Enum):
    SERVERDATA_AUTH = 3
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_RESPONSE_VALUE = 0


class Packet():
    def __init__(self, id, type, body):
        self.id = id
        self.type = type
        self.body = body

    @staticmethod
    def from_bytes(packet_data):
        return Packet(
            # ID (0 - 3)
            id=bytes_to_int(packet_data[0:4]),
            # Type (4 - 7)
            type=PacketType(bytes_to_int(packet_data[4:8])),
            # Body (8 -)
            body=packet_data[8:-1].decode('utf-8')
        )

    def to_bytes(self):
        return (
            # ID
            int_to_bytes(self.id) +
            # Type
            int_to_bytes(self.type.value) +
            # Body
            self.body.encode(encoding='utf-8') +
            # Empty String
            b'\x00'
        )

    def print(self):
        print('id:', self.id)
        print('type:', self.type)
        print('body:', self.body)
