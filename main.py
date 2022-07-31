from re import S
from Account import Account
from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA

# Inicializamos nuestra cadena de bloques
print("### Inicializamos nuestra blockchain")
blockchain = Blockchain()  # Tambien se crea el bloque genesis.

# Creamos dos cuenta que interactuaran con la blockchain.
brian = Account("Brian")
aaron = Account("Aaron")

# generamos un par de transacciones
tx1 = Transaction(brian, 20, aaron)
tx2 = Transaction(brian, 20, aaron)
tx3 = Transaction(aaron, 20, brian)
tx4 = Transaction(aaron, 20, brian)

# subimos las transacciones a la blockchain
blockchain.new_tx(brian, 35, aaron)
blockchain.new_tx(brian, 15, aaron)
blockchain.new_tx(aaron, 20, brian)
blockchain.new_tx(aaron, 15, brian)

# Imprimimos la cadena de bloques completa
blockchain.print_full_chain()

# quiero ver la firma de la primera transacttion
signature1 = tx1.sign_transaction()
signature3 = tx3.sign_transaction()

# verificacion
tx1.verify_transaction(signature1)
tx3.verify_transaction(signature3)

for block in blockchain.chain:
    for tx in block.list_of_transactions:
        print('-')
        print(tx.to_dict())
        print(tx.block)