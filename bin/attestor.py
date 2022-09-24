from Crypto.Hash import SHA256
import json

class Attestor():
    def __init__(self, validador) -> None:
        self.validator = validador

    def check_block(self, block):
        block_header = json.dumps(block.get_block_header_pos()).encode()
        block_hashed = SHA256.new(block_header)
        verifier = block.forger.validator.account.verifier
        try:
            verifier.verify(block_hashed, block.forger.block_signature)
            print(f"{self.validator.account.nickname}: Confirmo que la firma del bloque es correcta.")
            return True
        except:
            print("La firma es invalida.")
            return False
        #
        

class Attestors():
    def __init__(self, validators):
        self.group = [Attestor(validator) for validator in validators] 
    
    def attest(self, block):
        confirmations = []
        for attestor in self.group:
            confirmations.append(attestor.check_block(block))
        print('-----------------')
        # Se hace una division para cononcer cuantos votos minimos necesitamos, si el objetivo es superar el 75%
        minimun_votes = len(self.group) // 1.25
        if sum(confirmations) > minimun_votes:
            print('Confirmaciones suficientes para anadir el bloque.')
            return True
        else:
            print('Confirmaciones insuficientes para anadir el bloque.')
            return False