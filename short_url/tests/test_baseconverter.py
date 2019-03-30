# coding=utf-8
from django.test import TestCase
from short_url.baseconverter import BaseConverter


class TestBaseConverter(TestCase):

    def setUp(self):
        self.bin = BaseConverter("01")
        self.hex = BaseConverter("0123456789ABCDEF")
        self.base62 = BaseConverter('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz')

    def test_convert_to_simple_decimal(self):
        self.assertEqual(self.bin.to_decimal('0'), 0b0)
        self.assertEqual(self.bin.to_decimal('1'), 0b1)

        self.assertEqual(self.hex.to_decimal('0'), 0x0)
        self.assertEqual(self.hex.to_decimal('A'), 0xA)
        self.assertEqual(self.hex.to_decimal('F'), 0xF)

        self.assertEqual(self.base62.to_decimal("A"), 0)
        self.assertEqual(self.base62.to_decimal("Z"), 25)
        self.assertEqual(self.base62.to_decimal("0"), 26)
        self.assertEqual(self.base62.to_decimal("a"), 36)
        self.assertEqual(self.base62.to_decimal("z"), 61)

    def test_convert_from_simple_decimal(self):
        self.assertEqual(self.bin.from_decimal(0), "0")
        self.assertEqual(self.bin.from_decimal(1), "1")

        self.assertEqual(self.hex.from_decimal(0), "0")
        self.assertEqual(self.hex.from_decimal(10), "A")
        self.assertEqual(self.hex.from_decimal(15), "F")

        self.assertEqual(self.base62.from_decimal(0), "A")
        self.assertEqual(self.base62.from_decimal(10), "K")
        self.assertEqual(self.base62.from_decimal(25), "Z")
        self.assertEqual(self.base62.from_decimal(26), "0")
        self.assertEqual(self.base62.from_decimal(36), "a")
        self.assertEqual(self.base62.from_decimal(61), "z")

    def test_convert_to_decimal_with_positional(self):
        self.assertEqual(self.bin.to_decimal('10'), 0b10)
        self.assertEqual(self.bin.to_decimal('11'), 0b11)

        self.assertEqual(self.hex.to_decimal('10'), 0x10)
        self.assertEqual(self.hex.to_decimal('1A'), 0x1A)
        self.assertEqual(self.hex.to_decimal('F1'), 0xF1)

        self.assertEqual(self.base62.to_decimal("BA"), 62)
        self.assertEqual(self.base62.to_decimal("BZ"), 87)
        self.assertEqual(self.base62.to_decimal("B0"), 88)
        self.assertEqual(self.base62.to_decimal("Ba"), 98)
        self.assertEqual(self.base62.to_decimal("Bz"), 123)

    def test_convert_from_decimal_with_positional(self):

        self.assertEqual(self.bin.from_decimal(2), "10")
        self.assertEqual(self.bin.from_decimal(4), "100")

        self.assertEqual(self.hex.from_decimal(16), "10")
        self.assertEqual(self.hex.from_decimal(31), "1F")

        self.assertEqual(self.base62.from_decimal(62), "BA")
        self.assertEqual(self.base62.from_decimal(63), "BB")
        self.assertEqual(self.base62.from_decimal(123), "Bz")
        self.assertEqual(self.base62.from_decimal(124), "CA")
