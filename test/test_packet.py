from unittest import TestCase

from rcon.packet import Packet, PacketType


class TestPacket(TestCase):
    def test_from_bytes(self):
        packet_data = (
            # ID = 1
            b'\x01\x00\x00\x00' +
            # Type = SERVERDATA_AUTH(3)
            b'\x03\x00\x00\x00' +
            # Body
            b'password'
            # Empty String
            b'\x00'
        )
        packet = Packet.from_bytes(packet_data)

        # ID
        expected = 1
        actual = packet.id
        self.assertEqual(expected, actual)

        # Type
        expected = PacketType.SERVERDATA_AUTH
        actual = packet.type
        self.assertEqual(expected, actual)

        # Body
        expected = 'password'
        actual = packet.body
        self.assertEqual(expected, actual)

    def test_to_bytes(self):
        packet = Packet(
            id=1,
            type=PacketType.SERVERDATA_AUTH,
            body='password'
        )

        expected = (
            # ID = 1
            b'\x01\x00\x00\x00' +
            # Type = SERVERDATA_AUTH(3)
            b'\x03\x00\x00\x00' +
            # Body
            b'password'
            # Empty String
            b'\x00'
        )
        actual = packet.to_bytes()
        self.assertEqual(expected, actual)
