from datetime import datetime
from enum import Enum
from bin.account import Account
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256

class TxStatus(Enum):
    PENDIENTE = 0
    CONFIRMADA = 1
    DECLINADA = 2

class Transaction:
    def __init__(self, sender: Account, value: int, recipient: Account):
        self.sender = sender
        self.value = value
        self.recipient = recipient
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.block = None
        self.signature = None
        self.status = TxStatus.PENDIENTE
        # Al instanciarse una tx, esta debe reflejarse en la cuenta que la envia. (Sender)
        sender.list_of_all_transactions.append(self)


    def to_dict(self):
        """Exporta la transaccion en formato: dict."""
        return {
            'sender': self.sender.nickname,
            'recipient': self.recipient.nickname,
            'value': self.value,
            'time' : self.time}

    def sign_transaction(self): # (1)
        """Funcion que recibe un objeto transaccion y devuelve 
        la firma de la transaccion en bytes"""
        print("Firmando transaccion...")
        msg = str(self.to_dict()).encode()
        hash = SHA256.new(msg)
        signer = self.sender.signer
        signature = signer.sign(hash)
        # print("Signature:", binascii.hexlify(signature))
        self.signature = signature

    def verify_signature(self) -> bool: # (1)
        """Aqui se verifican las transacciones"""
        print("Verificando la firma de la transaccion...")
        msg = str(self.to_dict()).encode()
        hash = SHA256.new(msg)
        verifier = self.sender.verifier
        try:
            verifier.verify(hash, self.signature)
            print("La firma es valida.")
            return True
        except:
            print("La firma es invalida.")
            return False

    def change_status(self, new_status): # (3)
        if new_status == 'CONFIRMADA':
            self.status = TxStatus.CONFIRMADA
        elif new_status == 'PENDIENTE':
            self.status = TxStatus.PENDIENTE
        elif new_status == 'DECLINADA':
            self.status = TxStatus.DECLINADA