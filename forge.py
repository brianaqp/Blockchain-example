from Crypto.Hash import SHA256
import json

class Forge():
    def __init__(self, validator):
        self.validator = validator
    
    def verify_tx(self, holding_tx):
        """Funcion en la que el forjador verifica que las transacciones en espera sean
        validas para incluirlas en el bloque. La verificacion es igual que en PoW."""
        verified_tx = []
        for tx in holding_tx:
            if tx.verify_signature():
                verified_tx.append(tx)
        # Aqui deberia de haber una verifacion del doble-spend
        return verified_tx
    
    def sign_block(self, block) -> bool:
        """El forjador recibe un objeto bloque, lo firma con su llave privada."""
        print("Firmando transaccion...")
        #
        block_header = json.dumps(block.get_block_header()).encode() # Convert data to byte form so it can be hashed
        block_hashed = SHA256.new(block_header) 
        #
        signer = self.validator.signer
        signature = signer.sign(block_hashed)
        print("Signature:", signature)
        block.hash = signature
        