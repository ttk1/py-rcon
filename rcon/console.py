from rcon.connection import Connection
from rcon.packet import Packet, PacketType


class Console():
    def __init__(self, host, port=25575, password=''):
        if not password:
            raise Exception('Password is required!')

        self.id = 0
        self.conn = Connection(host, port)
        self.__login(password)

    def __get_id(self):
        self.id += 1
        return self.id

    def __login(self, password):
        req = Packet(
            id=self.__get_id(),
            type=PacketType.SERVERDATA_AUTH,
            body=password
        )
        self.conn.send_packet(req)
        res = self.conn.recv_packet()
        res.print()

    def command(self, command):
        req = Packet(
            id=self.__get_id(),
            type=PacketType.SERVERDATA_EXECCOMMAND,
            body=command
        )
        self.conn.send_packet(req)
        res = self.conn.recv_packet()
        res.print()

    def close(self):
        self.conn.close()
