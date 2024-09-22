from binomialmodel import *
from option import *

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