import binascii
from random import random
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Account:
    def __init__(self, nickname: str):
        self.nickname = nickname
        self.private_key = RSA.generate(1024)
        self.public_key = self.private_key.public_key()
        self.signer = PKCS1_v1_5.new(self.private_key)
        self.verifier = PKCS1_v1_5.new(self.public_key)

    @property
    def identity(self):
        return binascii.hexlify(self.public_key.exportKey(format="DER")).decode('ascii')
