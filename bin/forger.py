from Crypto.Hash import SHA256
import json

from bin.block import Block

class Forger():
    def __init__(self, validator):
        self.validator = validator
        self.block = None
        self.block_signature = None
    
    def verify_tx(self, holding_tx):
        """Funcion en la que el forjador verifica que las transacciones en espera sean
        validas para incluirlas en el bloque. La verificacion es igual que en PoW."""
        print('El forjador esta verificando las tx.')
        verified_tx = []
        for tx in holding_tx:
            if tx.verify_signature():
                print(tx.to_dict())
                verified_tx.append(tx)
        # Aqui deberia de haber una verifacion del doble-spend
        return verified_tx

    def create_a_block(self, _previous_hash, _verified_tx, _block_number):
        self.block = Block(_previous_hash, _verified_tx, _block_number)
    
    def sign_block(self) -> bool:
        """El forjador recibe un objeto bloque, lo firma con su llave privada."""
        print("### FIRMANDO EL BLOQUE")
        # Se anade el validador al bloque.
        self.block.forger = self
        # Se guarda la referencia del bloque en el objeto Forjador
        block_header = json.dumps(self.block.get_block_header_pos()).encode() # Convert data to byte form so it can be hashed
        block_hashed = SHA256.new(block_header) 
        #
        signer = self.validator.account.signer
        signature = signer.sign(block_hashed)
        self.block.hash = block_hashed.hexdigest()
        self.block_signature = signature
        print('### BLOQUE FIRMADO Y CON SU HASH ---')

    def broadcast_block(self):
        return self.block
        