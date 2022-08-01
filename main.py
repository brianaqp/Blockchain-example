import binascii
from re import S, X
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


# generamos y subimos las transacciones a la blockchain
blockchain.new_tx(brian, 35, aaron)
blockchain.new_tx(brian, 15, aaron)
blockchain.new_tx(aaron, 20, brian)
blockchain.new_tx(aaron, 15, brian)

# Imprimimos la cadena de bloques completa
# blockchain.print_full_chain()

# Ejemplo de una verificaion
# firma de un bloque
signature = blockchain.chain[1].list_of_transactions[0].signature

# verificacion con la verificacion
blockchain.chain[1].list_of_transactions[0].verify_transaction()

for block in blockchain.chain:
    for tx in block.list_of_transactions:
        print('-')
        # print(tx.signature)

# prueba
# x = binascii.hexlify(x).decode()
# print(x)