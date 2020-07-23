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

        expected = call('localhost', 25575)
        actual = Connection.call_args
        self.assertEqual(expected, actual)

        expected = 1
        actual = self.console._id
        self.assertEqual(expected, actual)

        expected = call('password')
        actual = _login.call_args
        self.assertEqual(expected, actual)

        # with port specitication
        Console('localhost', 'password', port=1234)

        expected = call('localhost', 1234)
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
        # reset call count of recv_packet
        self.conn.recv_packet.call_count = 0
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
        # reset call count of recv_packet
        self.conn.recv_packet.call_count = 0
        self.console.command('say hello')
        packet = self.conn.send_packet.call_args.args[0]

        # ID
        expected = 1234
        actual = packet.id
        self.assertEqual(expected, actual)

        # Type
        expected = PacketType.SERVERDATA_EXECCOMMAND
        actual = packet.type
        self.assertEqual(expected, actual)

        # Body
        expected = 'say hello'
        actual = packet.body
        self.assertEqual(expected, actual)

        # check call count of recv_packet
        expected = 1
        actual = self.conn.recv_packet.call_count
        self.assertEqual(expected, actual)

    def test_close(self):
        self.conn.close.call_count = 0
        self.console.close()

        expected = 1
        actual = self.conn.close.call_count
        self.assertEqual(expected, actual)
