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
        self._conn.send_packet(Packet(
            id=self._get_id(),
            type=PacketType.SERVERDATA_AUTH,
            body=password
        ))
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
        res = self._conn.recv_packet()
        res_body = res.body
        # Handle packet fragmentation
        if len(res_body) == 4096:
            self._conn.send_packet(Packet(
                id=self._get_id(),
                type=PacketType.INVALID_TYPE,
                body=''
            ))
            while True:
                res = self._conn.recv_packet()
                if res.id == req.id:
                    res_body += res.body
                else:
                    break
        return res_body

    def close(self):
        self._conn.close()
