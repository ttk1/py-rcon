# coidng: utf-8

from connection import Connection


class Console():
    def __init__(self, host, port=25575, password=''):
        self.conn = Connection(host, port)
        self.__login(password)

    def __login(self, password):
        pass
