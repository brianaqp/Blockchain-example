import json
from Block import Block
from Transaction import Transaction
from Account import Account
from Crypto.Hash import SHA256


class Blockchain:
    def __init__(self):
        self.chain = []
        self.tx_limit_per_block = 1
        self.holding_tx = []
        self.generate_genesis_block()

    def generate_genesis_block(self):
        """Inicializa el bloque genesis."""
        if len(self.chain) == 0: # Comprueba que la blockchain este vacia.
            tx = Transaction(Account("Genesis0"), 0, Account("Genesis01"))
            block = Block('0', [tx], 0)
            self.mine(block)
            self.chain.append(block)
        else:
            raise "Error: La Blockchain tiene que estar vacia."
    

    def new_tx(self, _sender: Account, _value: int, _receiver: Account):
        """Recibe los parametros para instanciar un objeto de 
        tipo Transaccion; verifica que sea una transaccion valida
        y lo anade a la holding list de la blockchain, 
        para luego ser parte de un bloque. """
        # 1. Instanciar un objeto transaccion.
        tx = Transaction(_sender, _value, _receiver)
        print("Nueva transaccion detectada... Estado: {}".format(tx.status.name))
        # 2. Esta transaccion necesita ser firmada (confirmada).
        tx.sign_transaction()
        # 3. La firma pasa a ser verificada, con la finalidad de comprobar que sea correcta.
        # 3.1. Si es correcta signifa que puede agregarse a un bloque
        if tx.verify_signature() == True:
            if len(self.holding_tx) < self.tx_limit_per_block: # Revisa si aun cabe en la lista de espera
                self.holding_tx.append(tx)
                print("Transaccion añadida a la espera.")
            if len(self.holding_tx) >= self.tx_limit_per_block: # Revisa si la lista de espera puede proceder
                tx_added = self.add_tx_to_block()
        # 3.2. Si no es correcta, se rechaza esta transaccion
        else:
            return 
            

    def add_tx_to_block(self):
        print("### Creando nuevo bloque ###")
        print('### Bloque No. ', len(self.chain))
        _block_number = len(self.chain)
        # try:
        block = Block(previous_hash=self.chain[-1].hash,list_of_transactions=self.holding_tx, block_number=_block_number)
        self.mine(block)
        self.chain.append(block)
        print("### Bloque creado. ###\n")
        self.holding_tx = []
        for tx in block.list_of_transactions:
            tx.block = _block_number
        self.verify_latest_tx()
        return True
        # except Exception as e:
        #  print("No se pudo crear el bloque. Error: ", e)


    def mine(self, block):
        """Funciona que mina el bloque. """
        print('Dentro de funcion minado...')
        # Primero obtenemos el string que contiene toda la informacion del bloque.
        block_header = json.dumps(block.get_block_header()).encode()
        block_hashed = SHA256.new(block_header)
        block_hash = block_hashed.hexdigest()
        # Proceso de minado
        # 1.Set difficulty, the difficulty_hash below is the equivalent of requiring 2 zeros at the front of the hash
        difficulty_hash = 0x0FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        difficult_decimal = 452312848583266388373324160190187140051835877600158453279131187530910662655
        # While the hash is bigger than or equal to the difficulty continue to iterate the nonce
        while int(block_hashed.hexdigest(), 16) >= difficulty_hash:
            block.nonce += 1 # Increment Nonce
            block_header = json.dumps(block.get_block_header()).encode() # Convert data to byte form so it can be hashed
            block_hashed = SHA256.new(block_header) 
            print('Nonce Guess: ', block.nonce)
            print('Resultant Hash: ' + str(block_hashed.hexdigest()))
            print('Decimal value of hash: ' + str(int(block_hashed.hexdigest(), 16)) + '\n')
            block_hash = block_hashed.hexdigest() # The hash of the blockheader with that nonce yields the block hash for that block
        print('Winner hash: ', block_hash)
        block.hash = block_hash


    def verify_latest_tx(self):
        "Verifica las ultimas transacciones del bloque añadido."
        latest_block = self.chain[-1]
        block_transactions = latest_block.list_of_transactions
        for tx in block_transactions:
            tx.change_status('CONFIRMADA')

    def print_full_chain(self):
        for block in self.chain:
            block.print_block_info()