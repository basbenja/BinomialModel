import numpy as np
import itertools

from option_type import *

def payoff(history, K):
    return max(np.mean(history) - K, 0)

n = 3
S0 = 20
u = 1.2
d = 0.8
I = 0.1
K = 18

S = np.zeros((2**n, n+1))
combinations = list(itertools.product([u, d], repeat=n))
for i in range(2**n):
    combination = [S0] + list(combinations[i])
    S[i, :] = np.cumprod(combination)

payoff = np.array(
    [payoff(S[j, :], K) for j in range(2**n)]
).reshape(-1, 1)

p = (1 + I - d) / (u - d)
q = 1 - p
V = np.zeros((2**n, n+1))
V[:, n] = payoff.flatten()
for j in range(n-1,-1,-1):
    for h in range(0, 2**n, 2**(n-j)):
        V[h, j] = discount(p*V[h,j+1] + q*V[h+2**(n-j-1),j+1], I)

Delta = np.zeros((2**(n-1), n))
for h in range(n):
    for j in range(0, 2**(n-1), 2**(n-h-1)):
        # print(j, 2**(n-h-1))
        Delta[j,h] = (V[2*j,h+1] - V[2*j+2**(n-h-1),h+1]) / (S[2*j,h+1] - S[2*j+2**(n-h-1),h+1])

np.set_printoptions(precision=5, suppress=True)

print(np.round(Delta, 5))