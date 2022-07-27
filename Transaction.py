import collections
from datetime import datetime
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import binascii

class Transaction:
    def __init__(self, sender: str, value: int, recipient: str):
        self.sender = sender
        self.value = value
        self.recipient = recipient
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def to_dict(self):
        if self.sender == "Genesis":
            account = "Genesis"
        else:
            account = self.sender.identity

        return collections.OrderedDict({
            "sender": account,
            "recipient": self.recipient,
            "value": self.value,
            "time": self.time
        })

    def sign_transaction(self):
        private_key = self.sender.private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')