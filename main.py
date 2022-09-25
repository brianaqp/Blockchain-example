from bin.account import Account
from bin.blockchain import Blockchain

# Inicializamos nuestra cadena de bloques
print("### Inicializamos nuestra blockchain")
blockchain = Blockchain()  # Tambien se crea el bloque genesis.

# Escojemos que protocolo queremos en nuestra blockchain
blockchain.set_consensus('PoW')

# Inicializamos el bloque genesis
blockchain.generate_genesis_block()

# Creamos dos cuenta que interactuaran con la blockchain.
brian = Account(100, "Brian")
aaron = Account(100, "Aaron")


# generamos y subimos las transacciones a la blockchain
blockchain.new_tx(brian, 101, aaron) # Esta brinca en error
blockchain.new_tx(brian, 20, aaron)
blockchain.new_tx(brian, 15, aaron)
blockchain.new_tx(brian, 1, aaron)
blockchain.new_tx(aaron, 31 , brian)

# Imprimimos la cadena de bloques completa
# blockchain.print_full_chain()

# Ejemplo de una verificaion
# firma de un bloque
signature = blockchain.chain[1].list_of_transactions[0].signature

# verificacion con la verificacion
blockchain.chain[1].list_of_transactions[0].verify_signature()

for block in blockchain.chain:
    for tx in block.list_of_transactions:
        print('-')
        print(tx.status)

# imprimir toda la blockchain
blockchain.print_full_chain()

# prueba
print()
print('cuenta: ', brian.nickname)
print('transacciones: ', brian.list_of_all_transactions)
print('ultima transacciones: ', brian.list_of_all_transactions[0].__dict__)
print(brian.balance)
print(aaron.balance)
print(blockchain.chain[-1].list_of_transactions[-1].signature)