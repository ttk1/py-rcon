from unittest import TestCase

from rcon.util import int_to_bytes, bytes_to_int


class TestUtil(TestCase):
    def test_int_to_bytes(self):
        res = int_to_bytes(1)

        expected = b'\x01\x00\x00\x00'
        actual = res
        self.assertEqual(expected, actual)

    def test_bytes_to_int(self):
        res = bytes_to_int(b'\x01\x00\x00\x00')

        expected = 1
        actual = res
        self.assertEqual(expected, actual)
