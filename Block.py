from datetime import datetime, date
from Account import Account


class Block:
    def __init__(
        self, previous_hash: str, list_of_transactions: list, block_number: int
    ):
        self.block_number = block_number
        self.previous_hash = previous_hash
        self.list_of_transactions = list_of_transactions
        self.nonce = 0

        # hash del bloque actual
        self.__block_hash = hash(
            f"{self.previous_hash}, {self.list_of_transactions}")

        # Anadir el time stamp
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        today = str(date.today())
        self.time_stamp = time + " " + today

    @property
    def block_hash(self):
        return self.__block_hash

    def print_block_info(self):
        print("-------------")
        print("Bloque No: ", self.block_number)
        print("Transacciones: ")
        self.tx_in_format()
        print("Hash anterior: ", self.previous_hash)
        print("Hash actual: ", self.block_hash)
        print("Time stamp: ", self.time_stamp)

    def tx_in_format(self):
        for tx in self.list_of_transactions:
            print(
                f"- {tx.sender.nickname} send {tx.value} to {tx.recipient.nickname}")
