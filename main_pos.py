from Account import Account
from validadores import Validador
from Blockchain import Blockchain

# Inicializamos nuestra cadena de bloques
print("### Inicializamos nuestra blockchain")
blockchain = Blockchain()  # Tambien se crea el bloque genesis.

# Escojemos que protocolo queremos en nuestra blockchain
blockchain.set_consensus('PoS')

# Creamos dos cuenta que interactuaran con la blockchain.
brian = Account("Brian")
aaron = Account("Aaron")

# Inicializamos a los Validadores de la red
charles = Validador(350)
edwin = Validador(500)
oliver = Validador(200)
erick = Validador(180)
sonia = Validador(275)

# Los incluimos en nuestra BlockChain
blockchain.set_validators((charles, edwin, oliver, erick, sonia))

# generamos y subimos las transacciones a la blockchain
blockchain.new_tx(brian, 101, aaron)
blockchain.new_tx(brian, 20, aaron)
blockchain.new_tx(brian, 15, aaron)
blockchain.new_tx(brian, 1, aaron)
blockchain.new_tx(aaron, 31 , brian)


# Ejemplo de una verificaion