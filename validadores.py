class Validador():
    def __init__(self, money, nickname):
        self.money = money
        self.nickname = nickname
        self.tokens = []

    def new_tokens(self, total_coins):
        # por cada moneda, se creara un token
        for every_coin in range(0, total_coins):
            self.tokens.append(Token(self))


class Token():
    def __init__(self, owner):
        self.owner = owner
