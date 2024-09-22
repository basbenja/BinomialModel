from binomialmodel import binomial
from option import *
from payoff_plot import payoff_plot
from stock import Stock
from utils import pretty_table

option = AsianOption(OptionType.CALL, K=18, T=3)
T = option.T
S0 = 20
u = 1.2
d = 0.8
I = 0.1

S, V, Delta = binomial(option, S0, u, d, I)

S = pretty_table(S, T+1, 'S')
V = pretty_table(V, T+1, 'V')
Delta = pretty_table(Delta, T, 'Delta')

print(S)
print(V)
print(Delta)


portfolio = [
    VanillaOption(type="put", K=100, T=5, position=PositionType.LONG, premium=10),
    Stock(position=PositionType.LONG, S0=100)
]
payoff_plot(portfolio, revenue=True)