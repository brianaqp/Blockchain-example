from bin.account import Account
from bin.blockchain import Blockchain

# Inicializamos nuestra cadena de bloques
print("### Inicializamos nuestra blockchain")
blockchain = Blockchain()  

# Escojemos que protocolo queremos en nuestra blockchain
blockchain.set_consensus('PoW')

# Inicializamos el bloque genesis
blockchain.generate_genesis_block()

# Creamos dos cuenta que interactuaran con la blockchain.
brian = Account(100, "Brian")
aaron = Account(10, "Aaron")

# generamos y subimos las transacciones a la blockchain
blockchain.new_tx(brian, 150, aaron) # La transacción no tiene balance suficiente
blockchain.new_tx(brian, 50, aaron) # Esta sí

# Ejemplo de una verificaion
# Firma de un bloque
print(blockchain.chain[1].list_of_transactions[0].signature)
print(blockchain.chain[1].list_of_transactions[0].status) 
print('---###---')
print(blockchain.chain[1].list_of_transactions[0].verify_signature())

# # Cuentas
print('Cuenta: ', brian.nickname)
print('Identity: ', brian.identity)
print('Transacciones: ', brian.list_of_all_transactions)
print('Ultima transaccion: ', brian.list_of_all_transactions[0].to_dict())