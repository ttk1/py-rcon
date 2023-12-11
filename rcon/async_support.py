import asyncio

from rcon.packet import Packet, PacketType
from rcon.util import int_to_bytes, bytes_to_int


class Connection():
    def __init__(self, host, port, timeout):
        self._host = host
        self._port = port
        self._timeout = timeout

    async def open(self):
        self._reader, self._writer = await asyncio.wait_for(
            asyncio.open_connection(self._host, self._port),
            timeout=self._timeout
        )

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()

    async def send_packet(self, packet: Packet):
        packet_data = packet.to_bytes()
        await self._write(
            int_to_bytes(len(packet_data)) +
            packet_data
        )

    async def recv_packet(self):
        size = bytes_to_int(await self._read(4))
        packet_data = await self._read(size)
        return Packet.from_bytes(packet_data)

    async def _write(self, data):
        self._writer.write(data)
        await self._writer.drain()

    async def _read(self, length):
        packet_data = await self._reader.read(length)
        if len(packet_data) < length:
            raise Exception('Received few bytes!')
        return packet_data


class Console():
    def __init__(self, host, password, port=25575, timeout=10):
        self._host = host
        self._port = port
        self._password = password
        self._timeout = timeout
        self._is_open = False

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, *_):
        await self.close()

    def _get_id(self):
        self._id += 1
        return self._id

    async def _login(self):
        await self._conn.send_packet(Packet(
            id=self._get_id(),
            type=PacketType.SERVERDATA_AUTH,
            body=self._password
        ))
        res = await self._conn.recv_packet()
        if res.id == 4294967295:
            raise Exception('Authentication failed: wrong password')

    async def open(self):
        self._res_bodies = {}
        self._waiting_packet_ids = []
        self._last_received_id = 0
        self._id = 0
        self._conn = Connection(self._host, self._port, self._timeout)
        await self._conn.open()
        await self._login()
        self._is_open = True

    async def close(self):
        await self._conn.close()
        self._is_open = False

    async def command(self, command):
        req = Packet(
            id=self._get_id(),
            type=PacketType.SERVERDATA_EXECCOMMAND,
            body=command
        )
        self._waiting_packet_ids.append(req.id)
        await self._conn.send_packet(req)
        # TODO: もっといい感じにしたい
        while True:
            if req.id not in self._waiting_packet_ids:
                return self._res_bodies.pop(req.id)
            if req.id == self._waiting_packet_ids[0]:
                res = await self._conn.recv_packet()
                if res.id in self._waiting_packet_ids:
                    if res.id in self._res_bodies:
                        self._res_bodies[res.id] += res.body
                    else:
                        self._res_bodies[res.id] = res.body
                    if len(res.body) == 4096:
                        if len(self._waiting_packet_ids) == 1:
                            await self._conn.send_packet(Packet(
                                id=self._get_id(),
                                type=PacketType.INVALID_TYPE,
                                body=''
                            ))
                    else:
                        self._waiting_packet_ids.remove(res.id)
                if self._last_received_id != res.id:
                    if self._last_received_id in self._waiting_packet_ids:
                        self._waiting_packet_ids.remove(self._last_received_id)
                    self._last_received_id = res.id
            else:
                await asyncio.sleep(1)

    def is_open(self):
        return self._is_open
