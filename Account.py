import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from tokens import Token

class Account:
    def __init__(self, nickname: str):
        self.nickname = nickname
        self.balance = 100
        self.list_of_all_transactions = []
        self.private_key = RSA.generate(1024)
        self.public_key = self.private_key.publickey()
        self.signer = PKCS115_SigScheme(self.private_key)
        self.verifier = PKCS115_SigScheme(self.public_key)

    @property
    def identity(self):
        return binascii.hexlify(self.public_key.exportKey(format="DER")).decode('ascii')

class Validator(Account):
    def __init__(self,  balance: int ,nickname: str):
        super().__init__(nickname)
        self.balance = balance
        self.nickname = nickname
        self.tokens = []

    def set_tokens(self, total_coins):
        for every_coin in range(0, total_coins):
            self.tokens.append(Token(self))

    def get_tokens(self):
        return len(self.tokens)
    
    
    
