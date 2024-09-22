from utils import PositionType

class Stock():
    def __init__(self, S0: float, position: PositionType):
        self.position = position
        self.S0 = S0

    def __str__(self):
        return f"{self.position.value.capitalize()} position in stock"

    def __repr__(self):
        return f"{self.position.value.capitalize()} position in stock"

    def payoff(self, S_T):
        return S_T if self.position == PositionType.LONG else -S_T

    def revenue(self, S_T):
        return self.payoff(S_T) - self.S0