import collections
from datetime import datetime
from re import S
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA, SHA256
from Crypto.PublicKey import RSA
import binascii

class Transaction:
    def __init__(self, sender: str, value: int, recipient: str):
        self.sender = sender
        self.value = value
        self.recipient = recipient
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def to_dict(self):
        """Exporta la transaccion en formato str, o dict."""
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'value': self.value,
            'time' : self.time}

    def sign_transaction(self):
        """Funcion que firma transacciones."""
        # obtenemos nuestro mensaje en utf8
        tx_data = self.to_dict() # type: dict
        tx_data_in_str = str(tx_data).encode() # type: str
        # obtenemos el hash del mensaje anterior
        h = SHA256.new(tx_data_in_str)
        # añadimos el "signer", objeto que nos ayuda a firmar
        signer = self.sender.signer # account signer with privatekey
        signature = signer.sign(h)
        # print(binascii.hexlify(signature))
        return signature

    def verify_transaction(self, signature):
        """Aqui se verifican las transacciones"""
        # obtenemos nuestro mensaje en utf8
        tx_data = self.to_dict() # type: dict
        tx_data_in_str = str(tx_data).encode() # type: str
        # obtenemos el hash del mensaje anterior
        h = SHA256.new(tx_data_in_str)
        # añadimos el "verifier", objeto que nos ayuda a verificar
        verifier = self.sender.verifier
        try:
            verifier.verify(h, signature)
            print("Signature is valid.")
            return h
        except:
            print("Signature is invalid.")

    def verify_transaction_wrong(self, signature):
        """Aqui se verifican las transacciones"""
        # obtenemos nuestro mensaje en utf8
        # tx_data = "string random" # type: dict
        tx_data = self.to_dict()
        tx_data_in_str = str(tx_data).encode() # type: str
        # obtenemos el hash del mensaje anterior
        h = SHA256.new(tx_data_in_str)
        # añadimos el "verifier", objeto que nos ayuda a verificar
        verifier = self.sender.verifier
        try:
            verifier.verify(h, signature)
            print("Signature is valid.")
            return h
        except:
            print("Signature is invalid.")
        
