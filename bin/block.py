from datetime import datetime, date
from bin.account import Account


class Block:
    def __init__(self, previous_hash: str, list_of_transactions: list, block_number: int):
        self.block_number = block_number
        self.previous_hash = previous_hash
        self.list_of_transactions = list_of_transactions
        self.nonce = 0
        self.hash = 0
        self.time_stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Cuando se instancia un bloque, le asigna el blocknumber a cada transaccion.
        for tx in self.list_of_transactions:
            tx.block = block_number
        # atributos utilizados con Proof of Stake.
        self.forger = None

    def get_block_header(self):
        """Funcion que retorna el encabezado del bloque."""
        return {
            'previous_block_hash':self.previous_hash,
            'nonce': self.nonce,
            'transactions':self.get_tx_in_format(),
        }
    
    def get_block_header_pos(self):
        return {
            'previous_block_hash':self.previous_hash,
            'nonce': self.nonce,
            'transactions':self.get_tx_in_format(),
            'forger': self.forger.validator.account.identity
            }


    def print_block_info(self):
        print("-------------")
        print("Bloque No: ", self.block_number)
        print("Transacciones: ")
        self.print_tx_in_format()
        print("Hash anterior: ", self.previous_hash)
        print("Hash actual: ", self.hash)
        print("Time stamp: ", self.time_stamp)

    def print_tx_in_format(self):
        for tx in self.list_of_transactions:
            print(
                f"- {tx.sender.nickname} send {tx.value} to {tx.recipient.nickname}")
    
    def get_tx_in_format(self):
        tx_list = []
        for tx in self.list_of_transactions:
            tx_in_str = f"{tx.sender.nickname} send {tx.value} to {tx.recipient.nickname}"
            tx_list.append(tx_in_str)
        return str(tx_list)