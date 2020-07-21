# coidng: utf-8

import socket

from rcon.packet import Packet


class Connection():
    def __init__(self, host, port):
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.sock.connect((host, port))

    @staticmethod
    def __from_bytes(value):
        return int.from_bytes(value, byteorder='little')

    def send_packet(self, packet: Packet):
        self.__write(packet.to_bytes())

    def recv_packet(self):
        size = self.__from_bytes(self.__read(4))
        packet_data = self.__read(size)
        return Packet.from_bytes(packet_data)

    def close(self):
        self.sock.close()

    def __write(self, data):
        self.sock.sendall(data)

    def __read(self, length):
        packet_data = self.sock.recv(length)
        if len(packet_data) < length:
            raise Exception('Received few bytes!')
        return packet_data
