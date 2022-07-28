import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme


class Account:
    def __init__(self, nickname: str):
        self.nickname = nickname
        self.private_key = RSA.generate(1024)
        self.public_key = self.private_key.publickey()
        self.signer = PKCS115_SigScheme(self.private_key)
        self.verifier = PKCS115_SigScheme(self.public_key)

    @property
    def identity(self):
        return binascii.hexlify(self.public_key.exportKey(format="DER")).decode('ascii')
