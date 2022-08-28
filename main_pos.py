from account import Account, Validator
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
charles = Validator(350, 'charles')
edwin = Validator(500, 'edwin')
oliver = Validator(200, 'oliver')
erick = Validator(90, 'erick')
sonia = Validator(275, 'sonia')

# Los incluimos en nuestra BlockChain
blockchain.set_validators((charles, edwin, oliver, erick, sonia))

# generamos y subimos las transacciones a la blockchain
blockchain.new_tx(brian, 10, aaron)


# Prueba
for validator in blockchain.validators.keys():
    print('Validor: ')
    print(validator.get_tokens())
    
        # print(token.owner.nickname)