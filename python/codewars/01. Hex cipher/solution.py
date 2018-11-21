import binascii
class HexCipher:
    @classmethod
    def encode(cls, s, n):
        return cls.encode((binascii.hexlify(s.encode('ascii')).decode('ascii')), n-1) if n>0 else s
    # Algorithm to encode the string here
    @classmethod
    def decode(cls, s, n):
        return cls.decode(binascii.unhexlify(s).decode('ascii'), n - 1) if n>0 else s