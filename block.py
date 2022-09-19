from datetime import datetime, date
from account import Account


class Block:
    def __init__(self, previous_hash: str, list_of_transactions: list, block_number: int):
        self.block_number = block_number
        self.previous_hash = previous_hash  
        self.list_of_transactions = list_of_transactions
        self.nonce = 0
        self.hash = 0
        self.merkle_root = 0
        for tx in self.list_of_transactions:
            tx.block = block_number
        # Anadir el time stamp
        self.time_stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def get_block_header(self) -> dict:
        """" Funcion que retorna un diccionario con el encabezado de nuestro bloque.
        """
        return {
            'previous_block_hash':self.previous_hash,
            'nonce': self.nonce,
            'transactions':self.get_tx_in_format()
        }

    def print_block_info(self) -> None:
        """Funcion que imprime la informacion del bloque, pero bonito."""
        print("-------------")
        print("Bloque No: ", self.block_number)
        print("Transacciones: ")
        self.print_tx_in_format()
        print("Hash anterior: ", self.previous_hash)
        print("Hash actual: ", self.hash)
        print("Time stamp: ", self.time_stamp)

    def print_tx_in_format(self) -> None:
        """Funcion que imprime de manera secuencial, y en formato,
        las transacciones del bloque."""
        for tx in self.list_of_transactions:
            print(
                f"- {tx.sender.nickname} send {tx.value} to {tx.recipient.nickname}")
    
    def get_tx_in_format(self) -> str:
        """Funcion que regresa una cadena de caracteres, de una lista que contiene las transacciones
        del bloque."""
        tx_list = []
        for tx in self.list_of_transactions:
            tx_in_str = f"{tx.sender.nickname} send {tx.value} to {tx.recipient.nickname}"
            tx_list.append(tx_in_str)
        return str(tx_list)