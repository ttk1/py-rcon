import socket

from rcon.packet import Packet
from rcon.util import bytes_to_int


class Connection():
    def __init__(self, host, port):
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.sock.connect((host, port))

    def send_packet(self, packet: Packet):
        self._write(packet.to_bytes())

    def recv_packet(self):
        size = bytes_to_int(self._read(4))
        packet_data = self._read(size)
        return Packet.from_bytes(packet_data)

    def close(self):
        self.sock.close()

    def _write(self, data):
        self.sock.sendall(data)

    def _read(self, length):
        packet_data = self.sock.recv(length)
        if len(packet_data) < length:
            raise Exception('Received few bytes!')
        return packet_data