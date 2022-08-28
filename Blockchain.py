import json
from Block import Block
from Transaction import Transaction
from tokens import Token
from forge import Forge
from account import Account
from Crypto.Hash import SHA256
from random import sample, choice
import sys


class Blockchain:
    def __init__(self):
        self.chain = []
        self.tx_limit_per_block = 1
        self.holding_tx = []
        self.generate_genesis_block()
        # Atributos propios de PoS
        self.stackers = {}
        self.total_stacked = 0
        self.validators = {}

    def generate_genesis_block(self):
        """Inicializa el bloque genesis."""
        if len(self.chain) == 0: # Comprueba que la blockchain este vacia.
            tx = Transaction(Account("Genesis0"), 0, Account("Genesis01"))
            block = Block('0', [tx], 0)
            self.mine(block)
            self.chain.append(block)
            block.list_of_transactions[0].change_status('CONFIRMADA')
        else:
            raise "Error: La Blockchain tiene que estar vacia."
    
    def set_consensus(self, protocol: str):
        if protocol not in ('PoW', 'PoS'):
            print('Seleccione un consenso de los dos disponibles.(PoW, PoS)')
            sys.exit()
        self.consensus = protocol

    def new_tx(self, _sender: Account, _value: int, _receiver: Account):
        """Recibe los parametros para instanciar un objeto de 
        tipo Transaccion; verifica que sea una transaccion valida
        y lo anade a la holding list de la blockchain, 
        para luego ser parte de un bloque. """
        # 0.5. Se debe verificar que quien manda la tx, tenga suficiente balance en su cuenta.
        if _value > _sender.balance: 
            print()
            print('No tienes suficiente balance en tu cuenta.')
            return
        # 1. Instanciar un objeto transaccion.
        tx = Transaction(_sender, _value, _receiver)
        # 1.2 Al momento de instanciar el objeto, le restamos a la cuenta principal
        # el dinero que envio.
        _sender.balance -= _value
        print()
        print("Nueva transaccion detectada... Estado: {}".format(tx.status.name))
        # 2. Esta transaccion necesita ser firmada (confirmada).
        tx.sign_transaction()
        # Aqui no se si sea correcto verificar la firma de una vez. Mas que nada por el consenso PoS.
        
        # 3. La firma pasa a ser verificada, con la finalidad de comprobar que sea correcta.
        # 3.1. Si es correcta signifa que puede agregarse a un bloque
        if tx.verify_signature() == True:
            if len(self.holding_tx) < self.tx_limit_per_block: # Revisa si aun cabe en la lista de espera
                self.holding_tx.append(tx)
                print("Transaccion añadida a la espera.")
            if len(self.holding_tx) >= self.tx_limit_per_block: # Revisa si la lista de espera puede proceder
                self.add_tx_to_block()
        else:
            return 
            

    def add_tx_to_block(self):
        """Funcion que toma las transacciones en espera y procede a implementarlas en un bloque, 
        para su posterior adision en la cadena de bloques."""
        print("### Creando nuevo bloque ###")
        print('### Bloque No. ', len(self.chain))
        _block_number = len(self.chain)
        # Consenso Proof of Work
        if self.consensus == 'PoW':
            block = Block(previous_hash=self.chain[-1].hash,list_of_transactions=self.holding_tx, block_number=_block_number)
            self.mine(block)
            self.chain.append(block)
            print("### Bloque creado. ###\n")
            self.holding_tx = []
            for tx in block.list_of_transactions:
                tx.block = _block_number
            self.verify_latest_tx()
            self.send_money_to_receivers()
        # Consenso Proof of Stake
        if self.consensus == 'PoS':
            print('En PoS:')
            forger, attestors = self.select_the_forger()
            print('Testigos: ', attestors)
            print('Forjador: ', forger)
            # En proceso de verificar las tx...
            verified_tx = forger.verify_tx(self.holding_tx)
            block = Block(previous_hash=self.chain[-1].hash, list_of_transactions=verified_tx, block_number=_block_number)
            forger.sign_block(block)


            
    def mine(self, block) -> None:
        """Funciona que mina el bloque.
        Funciona segun el protocolo de Proof of Stake. """
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
        """Pone como confirmadas las transacciones que ya forman parte de la cadena de
        Bloques original."""
        latest_block = self.chain[-1]
        block_transactions = latest_block.list_of_transactions
        for tx in block_transactions:
            tx.change_status('CONFIRMADA')

    def send_money_to_receivers(self):
        """Funcion que envia el dinero a los recipientes."""
        latest_block = self.chain[-1]
        block_transactions = latest_block.list_of_transactions
        for tx in block_transactions:
            # Condicional que cambia el estado de la transaccion a Declinada
            tx.change_status('DECLINADA')
            if tx.status.name == 'CONFIRMADA':
                tx.recipient.balance += tx.value
            if tx.status.name == 'DECLINADA':
                tx.sender.balance += tx.value
    
    def print_full_chain(self):
        for block in self.chain:
            block.print_block_info()

    # Apartir de aqui iniciare las funciones pertinentes a Proof of Stake.

    def set_validators(self, validators):
        """Funcion que determina los validadores de la red."""
        # La variable self.validators almacena las direcciones de los validadores
        # y el dinero que metieron en stack. (Similar a un SmartContract)
        for validator in validators:
            self.total_stacked += validator.balance
            self.stackers.update({validator: validator.balance})
            if validator.balance > 100: # Si stackea mas de 100 monedas, puede ser validador.
                self.validators.update({validator: validator.balance})
                validator.set_tokens(validator.balance)
            validator.balance -= validator.balance
        # No es lo mismo un validador que una persona que stackea su dinero. Por eso
        # existen 2 variables.

    def select_the_forger(self):
        """Funcion que selecciona que validador va a ser el forjador del nuevo bloque."""
        # Dentro de esta funcion, se va a disenar un algoritmo que escoja al siguiente forger, el siguiente ejemplo fue una implementacion propia, pero cada blockchain puede variar.
        # 
        # Cada validador tiene un 'stack' dentro del total en la blockchain. Cada
        # moneda que ingresaron es un 'ticket' que les puede dar la posibilidad de ser
        # el siguiente forjador del bloque.
        # La cantidad de tickets va a depender de la cantidad de monedas que ingresaron. ejemplo: Si el usuario stackeo 100 monedas, tiene 100 tickets dentro de la rifa.
        
        # Este algoritmo escojera un ticket al azar. El dueno del ticker sera el nuevo forger.
        # 1.- Lista que almacenara todos los tickets de la rifa
        pool = []
        # 2.- Bucle que recorrera a cada validador, y añadara sus tokens a la lista general.
        for validator in self.validators:
            pool += validator.tokens
        # 3.- Se revuelve la lista. (Como si fuera un sorteo.)
        print('Acumulando los tokens de los participantes de la lista...')
        print(len(pool), '- tokens acumulados.')
        print('Revolviendo la lista...')
        pool = sample(pool, len(pool))
        print('Lista revuelta!')
        # Funcion que revisa los tokens de cada quien. Estaria chido ponerla como funcion aparte.
        contador = 0
        for validator in self.validators.keys():
            for token in pool:
                if token.owner.nickname == validator.nickname:
                    contador += 1
            print(validator.nickname, contador)
            contador = 0
        # Fin de la validacion
        # Aqui deberia de ir algo estilo, escojer el ticket ganador.
        ticket_winner = choice(pool)
        forger = Forge(ticket_winner.owner)
        print(forger)
        print(f'El forjador del nuevo bloque sera... {forger.validator}')
        # los validadores no ganadores del sorteo pasan a ser testigos.
        # los testigos estan encargados de revisar que el forjador haga lo correcto
        attestors = [validator for validator in self.validators]
        # se remueve el forjador, asi solo quedan los testigos
        attestors.remove(forger.validator)
        return forger, attestors