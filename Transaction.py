from datetime import datetime
from enum import Enum
from telnetlib import STATUS
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

class Status(Enum):
    def __init__(self) -> None:
        super().__init__()
        self.PENDING = 0
        self.CONFIRMED = 1
        self.DECLINED = 2

status = Status(0)


class Transaction:
    def __init__(self, sender: str, value: int, recipient: str):
        self.sender = sender
        self.value = value
        self.recipient = recipient
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.block = None
        self.signature = None
        self.status = None


    def to_dict(self):
        """Exporta la transaccion en formato: dict."""
        return {
            'sender': self.sender.nickname,
            'recipient': self.recipient.nickname,
            'value': self.value,
            'time' : self.time}

    def sign_transaction(self):
        """Recibe un objeto transaccion y devuelve la firma. en bytes"""
        msg = str(self.to_dict()).encode()
        hash = SHA256.new(msg)
        signer = self.sender.signer
        signature = signer.sign(hash)
        # print("Signature:", binascii.hexlify(signature))
        self.signature = signature

    def verify_transaction(self):
        """Aqui se verifican las transacciones"""
        msg = str(self.to_dict()).encode()
        hash = SHA256.new(msg)
        verifier = self.sender.verifier
        try:
            verifier.verify(hash, self.signature)
            print("Signature is valid.")
            return True
        except:
            print("Signature is invalid.")
            return False
