# coding=utf-8


class BaseConverter(object):
    """
    10进制正整数与任意进制转换
    """

    def __init__(self, digits):
        self.digits = digits
        self.base = len(digits)

    def from_decimal(self, num):
        if num < 0:
            raise ValueError("Converter only takes positive num")
        enc = ''
        while num >= self.base:
            num, mod = divmod(num, self.base)
            enc = self.digits[mod] + enc
        enc = self.digits[num] + enc
        return enc

    def to_decimal(self, s):
        neg = 0
        decoded = 0
        multi = 1
        while len(s) > 0:
            decoded += multi * self.digits.index(s[-1:])
            multi = multi * self.base
            s = s[:-1]
        if neg:
            decoded = -decoded
        return decoded


base62 = BaseConverter('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz')
