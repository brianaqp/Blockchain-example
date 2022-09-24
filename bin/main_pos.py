from account import Account, Validator
from blockchain import Blockchain

# Inicializamos nuestra cadena de bloques
print("### Inicializamos nuestra blockchain")
blockchain = Blockchain()  # Tambien se crea el bloque genesis.

# Escojemos que protocolo queremos en nuestra blockchain
blockchain.set_consensus('PoS')

# inicializamos el bloque genesis
blockchain.generate_genesis_block()

# Creamos dos cuenta que interactuaran con la blockchain.
brian = Account(100, "Brian")
aaron = Account(100, "Aaron")

# Inicializamos 5 cuentas que quieran ser validadores
charles = Account(350, 'charles')
edwin = Account(500, 'edwin')
oliver = Account(200, 'oliver')
erick = Account(90, 'erick')
sonia = Account(275, 'sonia')

# Los incluimos en nuestra BlockChain
blockchain.set_validators((charles, edwin, oliver, erick, sonia))

# generamos y subimos las transacciones a la blockchain
blockchain.new_tx(brian, 20, aaron)
blockchain.new_tx(brian, 20, aaron)
print(brian.balance, aaron.balance)
print(blockchain.chain[-2].forger.validator.account.nickname)
print(blockchain.chain[-1].forger.validator.account.nickname)

print(blockchain.stackers)