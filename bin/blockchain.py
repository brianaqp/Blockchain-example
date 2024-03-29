import atexit
import json
from bin.block import Block
from bin.transaction import Transaction, TxStatus
from bin.tokens import Token
from bin.attestor import Attestor, Attestors
from bin.forger import Forger
from bin.account import Validator, Account
from Crypto.Hash import SHA256
from random import sample, choice
import sys


class Blockchain:
    def __init__(self):
        self.protocol = None
        self.chain = []
        self.tx_limit_per_block = 1
        self.holding_tx = []
        # Atributos propios de PoS
        self.total_stacked = 0
        self.validators = {}
        self.last_block = None

    def generate_genesis_block(self):
        """Inicializa el bloque genesis."""
        print("Inicializando bloque genesis...")
        if len(self.chain) == 0: # Comprueba que la blockchain este vacia.
            tx = Transaction(Account(0, "Genesis0"), 0, Account(0, "Genesis01"))
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
            print('\n### --- No tienes suficiente balance en tu cuenta. --- ###')
            print('### --- La transacción no puede agregarse a la red. --- ###\n')

            return
        print('Nueva transaccion detectada... Balance suficiente.')
        # 1. Instanciar un objeto transaccion.
        tx = Transaction(_sender, _value, _receiver)
        # 1.2 Al momento de instanciar el objeto, le restamos a la cuenta principal
        # el dinero que envio.
        _sender.balance -= _value
        print("Estado: {}".format(tx.status.name))
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
            print('En PoW')
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
            forger, validators_with_out_forger = self.select_the_forger()
            # Los validadores no seleccionados pasan a ser objetos Attestors.
            attestors = Attestors(validators_with_out_forger)
            print('Testigos: ', [attestor.validator.account.nickname for attestor in attestors.group])
            print('Forjador: ', [forger.validator.account.nickname])
            # En proceso de verificar las tx...
            verified_tx = forger.verify_tx(self.holding_tx)
            forger.create_a_block(self.chain[-1].hash, verified_tx, _block_number)
            forger.sign_block()
            # el forjador manda el bloque a la red
            print('### Enviando el bloque a la red...')
            self.last_block = forger.broadcast_block()
            print('### Iniciando atestiguamiento del bloque...')
            if attestors.attest(self.last_block):
                self.chain.append(self.last_block)
                print("### Bloque creado. ###\n")
                self.holding_tx = []
                for tx in self.last_block.list_of_transactions:
                    tx.block = _block_number
                self.verify_latest_tx()
                self.send_money_to_receivers()
            else:
                print('No se pudo incluir el bloque.')
                return
            # Cada testigo va a 'atestiguar' que el forjador verifico correctamente las transacciones y su bloque esta bien hecho.
            # Si esta correcto, daran su 'confirmacion'. 
            # Se necesita que el 75% de los testigos den su confirmacion positiva para anexar el bloque a la cadena de bloques.
            

            
    def mine(self, block) -> None:
        """Funciona que mina el bloque.
        Funciona segun el protocolo de Proof of Stake. """
        print('Dentro de funcion mine...')
        # Primero obtenemos el string que contiene toda la informacion del bloque.
        block_header = json.dumps(block.get_block_header()).encode()
        block_hashed = SHA256.new(block_header)
        block_hash = block_hashed.hexdigest()
        # Proceso de minado
        if self.consensus == 'PoW':
        # 1. Dificultad
            difficulty_hash = 0x0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            difficult_decimal = 1766847064778384329583297500742918515827483896875618958121606201292619775 # equivalencia de difficulty_hash en decimal
            # Sigue hasta que el hash sea menor o igual a la dificultad
            while int(block_hashed.hexdigest(), 16) >= difficulty_hash:
                block.nonce += 1 # Incremento del Nonce 
                block_header = json.dumps(block.get_block_header()).encode() # Se convierte el valor a strin
                block_hashed = SHA256.new(block_header) # Pdd. Va a salir distinto por el cambio de nonce!
                block_hash = block_hashed.hexdigest() # El bloque guarda el hash en hexadecimal

            print('Nonce Guess: ', block.nonce)
            print('Resultant Hash: ' + str(block_hashed.hexdigest()))
            print('Decimal value of hash: ' + str(int(block_hashed.hexdigest(), 16)) + '\n')
            block.hash = block_hash
            
        if self.consensus == 'PoS':
            # Para pos vamos a saltar el proceso de minado
            block.hash = block_hash
            print("Hash añadido al bloque genesis...")

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
            # tx.change_status('DECLINADA')
            if tx.status.name == 'CONFIRMADA':
                tx.recipient.balance += tx.value
            if tx.status.name == 'DECLINADA':
                tx.sender.balance += tx.value
    
    def print_full_chain(self):
        for block in self.chain:
            block.print_block_info()

    # Apartir de aqui iniciare las funciones pertinentes a Proof of Stake.

    def set_validators(self, accounts):
        """Funcion que determina los validadores de la red."""
        for account in accounts:
            if account.balance >= 100: # Si tiene igual o mas de 100 en balance, puede ser un validador.
                new_validator = Validator(account) # Se crea un validador mandando la cuenta
                self.total_stacked += new_validator.account.balance # Se anade el balance de la cuenta como al stack total de la red
                new_validator.set_tokens(new_validator.account.balance) # Se anaden tokens por cuenta
                self.validators.update({new_validator: new_validator.account.balance}) # se anade en un diccionario un registro de {cuenta: balance ingresado}
                new_validator.account.balance -= new_validator.account.balance # Se resta el balance de la cuenta

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
        print('Acumulando los tokens de los validadores en el servidor actual...')
        print(len(pool), '- tokens acumulados.')
        print('Revolviendo la lista...')
        pool = sample(pool, len(pool))
        print('Lista revuelta!')
        # Funcion que revisa los tokens de cada quien. Estaria chido ponerla como funcion aparte.
        contador = 0
        for validator in self.validators.keys():
            for token in pool:
                if token.owner.account.nickname == validator.account.nickname:
                    contador += 1
            print(validator.account.nickname, contador)
            contador = 0
        # Fin de la validacion
        # Aqui deberia de ir algo estilo, escojer el ticket ganador.
        ticket_winner = choice(pool)
        forger = Forger(ticket_winner.owner)
        print(f'El forjador del nuevo bloque sera... {forger.validator.account.nickname}')
        # los validadores no ganadores del sorteo pasan a ser testigos.
        # los testigos estan encargados de revisar que el forjador haga lo correcto
        validators_with_out_forger = [validator for validator in self.validators]
        # se remueve el forjador, asi solo quedan los testigos
        validators_with_out_forger.remove(forger.validator)
        return forger, validators_with_out_forger