from rcon.connection import Connection
from rcon.packet import Packet, PacketType


class Console():
    def __init__(self, host, password, port=25575, timeout=10):
        self._conn = Connection(host, port, timeout)
        self._id = 0
        self._login(password)

    def _get_id(self):
        self._id += 1
        return self._id

    def _login(self, password):
        req = Packet(
            id=self._get_id(),
            type=PacketType.SERVERDATA_AUTH,
            body=password
        )
        self._conn.send_packet(req)
        res = self._conn.recv_packet()
        if res.id == 4294967295:
            raise Exception('Authentication failed: wrong password')

    def command(self, command):
        req = Packet(
            id=self._get_id(),
            type=PacketType.SERVERDATA_EXECCOMMAND,
            body=command
        )
        self._conn.send_packet(req)
        return self._conn.recv_packet()

    def close(self):
        self._conn.close()
