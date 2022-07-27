from numpy import block
from Account import Account
from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction
from Crypto.PublicKey import RSA

# Inicializamos nuestra cadena de bloques
print("### Inicializamos nuestra blockchain")
blockchain = Blockchain() # Tambien se crea el bloque genesis.

# Crearemos una cuenta que interactuara con la blockchain
main_account = Account("Fulanito")
print(main_account.nickname)
other_account = Account("Mungano")

# generamos un par de transacciones
tx1 = Transaction(main_account, 20, other_account)
tx2 = Transaction(main_account, 20, other_account)
tx3 = Transaction(other_account, 20, main_account)
tx4 = Transaction(other_account, 20, main_account)

# subimos las transacciones a la blockchain
blockchain.new_tx(tx1)
blockchain.new_tx(tx2)
blockchain.new_tx(tx3)
blockchain.new_tx(tx4)

# Imprimimos la cadena de bloques completa
blockchain.print_full_chain()
