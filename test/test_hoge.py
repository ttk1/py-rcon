from unittest import TestCase
from unittest.mock import Mock, patch, call

from rcon import hoge


class TestHoge(TestCase):
    @patch('rcon.hoge.print')
    def test_fuga(self, _print):
        hoge.fuga()

        expected = call('fugafuga')
        actual = _print.call_args
        self.assertEqual(expected, actual)
