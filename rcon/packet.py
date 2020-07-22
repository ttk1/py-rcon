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

    @classmethod
    def from_bytes(cls, packet_data):
        offset = 0
        # ID
        id = bytes_to_int(packet_data[offset:offset+4])
        offset += 4
        # Type
        type = PacketType(bytes_to_int(packet_data[offset:offset+4]))
        offset += 4
        # Body
        body = packet_data[offset:].decode('utf-8')
        return cls(
            id=id,
            type=type,
            body=body
        )

    def to_bytes(self):
        packet_data = b''
        # ID
        packet_data += int_to_bytes(self.id)
        # Type
        packet_data += int_to_bytes(self.type.value)
        # Body
        packet_data += self.body.encode(encoding='utf-8')
        # Empty String
        packet_data += b'\x00'
        # Size
        packet_data = int_to_bytes(len(packet_data)) + packet_data
        return packet_data

    def print(self):
        print('id:', self.id)
        print('type:', self.type)
        print('body:', self.body)
