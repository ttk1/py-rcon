# coidng: utf-8

from enum import Enum


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
        id = cls.__from_bytes(packet_data[offset:offset+4])
        offset += 4
        # Type
        type = PacketType(cls.__from_bytes(packet_data[offset:offset+4]))
        offset += 4
        # Body
        body = packet_data[offset:].decode('utf-8')
        return Packet(
            id=id,
            type=type,
            body=body
        )

    @staticmethod
    def __to_bytes(value):
        return value.to_bytes(4, byteorder='little')

    @staticmethod
    def __from_bytes(value):
        return int.from_bytes(value, byteorder='little')

    def to_bytes(self):
        packet_data = b''
        # ID
        packet_data += self.__to_bytes(self.id)
        # Type
        packet_data += self.__to_bytes(self.type.value)
        # Body
        packet_data += self.body.encode(encoding='utf-8')
        # Empty String
        packet_data += b'\x00'
        # Size
        packet_data = self.__to_bytes(len(packet_data)) + packet_data
        return packet_data

    def print(self):
        print('id:', self.id)
        print('type:', self.type)
        print('body:', self.body)
