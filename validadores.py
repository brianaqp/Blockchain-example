class Validador():
    def __init__(self, money, nickname):
        self.money = money
        self.nickname = nickname
        self.tokens = []

    def set_tokens(self, total_coins):
        for every_coin in range(0, total_coins):
            self.tokens.append(Token(self))

    def get_tokens(self):
        return len(self.tokens)
        

class Token():
    def __init__(self, owner):
        self.owner = owner
