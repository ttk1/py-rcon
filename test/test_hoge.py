# coidng: utf-8

from unittest import TestCase
from unittest.mock import Mock, patch, call

from rcon import hoge


class TestHoge(TestCase):
    @patch('rcon.hoge.print')
    def test_hoge(self, _print):
        hoge.hoge()

        expected = call('hoge')
        actual = _print.call_args
        self.assertEqual(expected, actual)
