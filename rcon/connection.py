# coidng: utf-8

import socket


class Connection():
    def __init__(self, host, port):
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.sock.connect((host, port))

    def close(self):
        self.sock.close()

    def write(self, data):
        pass

    def read(self, length):
        pass
