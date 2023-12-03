from unittest import TestCase
from unittest.mock import patch, Mock, call

from rcon.connection import Connection


class TestConnection(TestCase):
    @patch('rcon.connection.socket')
    def setUp(self, socket):
        sock = Mock()
        socket.socket.return_value = sock
        self.sock = sock
        self.conn = Connection('localhost', 1234, 10)

    def test_host_and_port(self):
        expected = call(('localhost', 1234))
        actual = self.sock.connect.call_args
        self.assertEqual(expected, actual)

    def test_send_packet(self):
        packet = Mock()
        packet.to_bytes.return_value = b'test'
        self.conn._write = Mock()
        self.conn.send_packet(packet)

        expected = call(b'\x04\x00\x00\x00test')
        actual = self.conn._write.call_args
        self.assertEqual(expected, actual)

    @patch('rcon.connection.Packet')
    def test_recv_packet(self, Packet):
        _read = Mock()
        _read.side_effect = [
            # size
            b'\x04\x00\x00\x00',
            b'test'
        ]
        self.conn._read = _read
        self.conn.recv_packet()

        expected = [
            call(4),
            call(4)
        ]
        actual = _read.call_args_list
        self.assertEqual(expected, actual)

        expected = call(b'test')
        actual = Packet.from_bytes.call_args
        self.assertEqual(expected, actual)

    def test_close(self):
        expected = 0
        actual = self.sock.close.call_count
        self.assertEqual(expected, actual)

        self.conn.close()

        expected = 1
        actual = self.sock.close.call_count
        self.assertEqual(expected, actual)

    def test_write(self):
        data = b'test'
        self.conn._write(data)

        expected = call(b'test')
        actual = self.sock.sendall.call_args
        self.assertEqual(expected, actual)

    def test_read(self):
        self.sock.recv.return_value = b'test'
        res = self.conn._read(4)

        expected = b'test'
        actual = res
        self.assertEqual(expected, actual)

    def test_read_few_bytes(self):
        self.sock.recv.return_value = b'test'

        with self.assertRaises(Exception) as cm:
            self.conn._read(5)

        self.assertEqual('Received few bytes!', cm.exception.args[0])
