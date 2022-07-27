from Account import Account
from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction
from Crypto.PublicKey import RSA

# Inicializamos nuestra cadena de bloques
print("### Inicializamos nuestra blockchain")
blockchain = Blockchain()  # Tambien se crea el bloque genesis.

# Crearemos una cuenta que interactuara con la blockchain
brian = Account("Brian")
print(brian.nickname)
aaron = Account("Aaron")


# generamos un par de transacciones
tx1 = Transaction(brian, 20, aaron)
signature1 = tx1.sign_transaction()
tx2 = Transaction(brian, 20, aaron)
tx3 = Transaction(aaron, 20, brian)
tx4 = Transaction(aaron, 20, brian)

# subimos las transacciones a la blockchain
blockchain.new_tx(tx1)
blockchain.new_tx(tx2)
blockchain.new_tx(tx3)
blockchain.new_tx(tx4)

# Imprimimos la cadena de bloques completa
blockchain.print_full_chain()

# quiero ver la firma de la primera transacttion
print(signature1)