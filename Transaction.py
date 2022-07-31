from datetime import datetime
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

class Transaction:
    def __init__(self, sender: str, value: int, recipient: str):
        self.sender = sender
        self.value = value
        self.recipient = recipient
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.block = None

    def to_dict(self):
        """Exporta la transaccion en formato: dict."""
        return {
            'sender': self.sender.nickname,
            'recipient': self.recipient.nickname,
            'value': self.value,
            'time' : self.time}

    def sign_transaction(self):
        """Funcion que firma transacciones."""
        msg = str(self.to_dict()).encode()
        hash = SHA256.new(msg)
        signer = self.sender.signer
        signature = signer.sign(hash)
        print("Signature:", binascii.hexlify(signature))
        return signature

    def verify_transaction(self, signature):
        """Aqui se verifican las transacciones"""
        msg = str(self.to_dict()).encode()
        hash = SHA256.new(msg)
        verifier = self.sender.verifier
        try:
            verifier.verify(hash, signature)
            print("Signature is valid.")
        except:
            print("Signature is invalid.")

    def verify_transaction_wrong(self, signature):
        """Aqui se verifican las transacciones"""
        msg = str(str(self.to_dict())+"a").encode()
        hash = SHA256.new(msg)
        verifier = PKCS115_SigScheme(self.sender.public_key)
        try:
            verifier.verify(hash, signature)
            print("Signature is valid.")
        except:
            print("Signature is invalid.")
        
