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