from unittest import TestCase
from unittest.mock import patch, Mock, call

from rcon.console import Console
from rcon.packet import PacketType


class TestConsole(TestCase):
    @patch('rcon.console.Connection')
    def setUp(self, Connection):
        conn = Mock()
        Connection.return_value = conn
        self.conn = conn
        self.console = Console('localhost', 'password')

    @patch('rcon.console.Connection')
    @patch('rcon.console.Console._login')
    def test_init(self, _login, Connection):
        Console('localhost', 'password')

        expected = call('localhost', 25575, 10)
        actual = Connection.call_args
        self.assertEqual(expected, actual)

        expected = 1
        actual = self.console._id
        self.assertEqual(expected, actual)

        expected = call('password')
        actual = _login.call_args
        self.assertEqual(expected, actual)

        # with port and timeout specification
        Console('localhost', 'password', port=1234, timeout=123)

        expected = call('localhost', 1234, 123)
        actual = Connection.call_args
        self.assertEqual(expected, actual)

    def test_get_id(self):
        self.console._id = 1234
        res = self.console._get_id()

        expected = 1235
        actual = res
        self.assertEqual(expected, actual)

        actual = self.console._id
        self.assertEqual(expected, actual)

    @patch('rcon.console.Console._get_id')
    def test_login(self, _get_id):
        _get_id.return_value = 1234
        self.conn.reset_mock()
        self.console._login('password')
        packet = self.conn.send_packet.call_args.args[0]

        # ID
        expected = 1234
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

        # check call count of recv_packet
        expected = 1
        actual = self.conn.recv_packet.call_count
        self.assertEqual(expected, actual)

    @patch('rcon.console.Console._get_id')
    def test_command(self, _get_id):
        _get_id.return_value = 1234
        self.conn.reset_mock()
        res_packet = Mock()
        res_packet.body = 'command response'
        self.conn.recv_packet.return_value = res_packet
        self.console.command('command')
        req_packet = self.conn.send_packet.call_args.args[0]

        # ID
        expected = 1234
        actual = req_packet.id
        self.assertEqual(expected, actual)

        # Type
        expected = PacketType.SERVERDATA_EXECCOMMAND
        actual = req_packet.type
        self.assertEqual(expected, actual)

        # Body
        expected = 'command'
        actual = req_packet.body
        self.assertEqual(expected, actual)

        # check call count of recv_packet
        expected = 1
        actual = self.conn.recv_packet.call_count
        self.assertEqual(expected, actual)

    @patch('rcon.console.Console._get_id')
    def test_handle_fragmentation(self, _get_id):
        _get_id.side_effect = [1001, 1002]
        self.conn.reset_mock()

        res_packet1 = Mock()
        res_packet1.body = 'a' * 4096
        res_packet1.id = 1001
        res_packet2 = Mock()
        res_packet2.body = 'b' * 1000
        res_packet2.id = 1001
        res_packet3 = Mock()
        res_packet3.body = 'error response'
        res_packet3.id = 1002

        self.conn.recv_packet.side_effect = [
            res_packet1, res_packet2, res_packet3
        ]
        res_body = self.console.command('command')
        second_req_packet = self.conn.send_packet.call_args_list[1].args[0]

        # check second request packet type
        expected = PacketType.INVALID_TYPE
        actual = second_req_packet.type
        self.assertEqual(expected, actual)

        # check merged response
        expected = 'a' * 4096 + 'b' * 1000
        actual = res_body
        self.assertEqual(expected, actual)

    def test_close(self):
        self.conn.reset_mock()
        self.console.close()

        expected = 1
        actual = self.conn.close.call_count
        self.assertEqual(expected, actual)
