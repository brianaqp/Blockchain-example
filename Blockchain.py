from Block import Block
from Transaction import Transaction
from Account import Account


class Blockchain:
    def __init__(self):
        self.chain = []
        self.tx_limit_per_block = 2
        self.holding_tx = []
        self.generate_genesis_block()

    def generate_genesis_block(self):
        if len(self.chain) == 0:
            tx = Transaction(Account("Genesis0"), 0, Account("Genesis1"))
            self.holding_tx.append(tx)
            self.chain.append(Block("0", self.holding_tx, 0))
            self.holding_tx = []
        else:
            raise "Error: La Blockchain tiene que estar vacia."
    
    def new_tx(self, _tx):
        tx = _tx
        if len(self.holding_tx) < self.tx_limit_per_block:
            self.holding_tx.append(tx)
            print("Transaccion anadida a la espera.")
        if len(self.holding_tx) >= self.tx_limit_per_block:
            self.add_tx_to_block()
            

    def add_tx_to_block(self):
        print("### Creando nuevo bloque ###")
        block = Block(previous_hash=self.chain[-1].block_hash, list_of_transactions=self.holding_tx, block_number=len(self.chain)) 
        self.chain.append(block)
        self.holding_tx = []

    def print_full_chain(self):
        for block in self.chain:
            block.print_block_info()