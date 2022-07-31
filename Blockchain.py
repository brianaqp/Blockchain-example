from Block import Block
from Transaction import Transaction
from Account import Account


class Blockchain:
    def __init__(self):
        self.chain = []
        self.tx_limit_per_block = 1
        self.holding_tx = []
        self.generate_genesis_block()

    def generate_genesis_block(self):
        """Inicializa el bloque genesis."""
        if len(self.chain) == 0:
            tx = Transaction(Account("Genesis0"), 0, Account("Genesis01"))
            tx.block = 0
            self.chain.append(Block("0", [tx], 0))
        else:
            raise "Error: La Blockchain tiene que estar vacia."
    

    def new_tx(self, _sender: Account, _value: int, _receiver: Account):
        """Recibe los parametros para instanciar un objeto de 
        tipo Transaccion; la añade a la holding list y dependiendo
        del status o de la blockchain, se añade a un bloque. """
        tx = Transaction(_sender, _value, _receiver)
        if len(self.holding_tx) < self.tx_limit_per_block:
            self.holding_tx.append(tx)
            print("Transaccion añadida a la espera.")
        if len(self.holding_tx) >= self.tx_limit_per_block:
            self.add_tx_to_block()
            

    def add_tx_to_block(self):
        print("### Creando nuevo bloque ###")
        _block_number = len(self.chain)
        try:
            block = Block(previous_hash=self.chain[-1].block_hash, list_of_transactions=self.holding_tx, blocl_number=_block_number)
            self.chain.append(block)
            self.holding_tx = []
            for tx in block.list_of_transactions:
                tx.block = _block_number
        except:
            print("No se pudo crear el bloque. Error.")

    def print_full_chain(self):
        for block in self.chain:
            block.print_block_info()