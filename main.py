import numpy as np
import itertools

from option_type import OptionType, discount, pretty_table

def binomial(
    option: OptionType,
    n: int,
    S0: float,
    u: float,
    d: float,
    K: float,
    I: float,
    hist_dependent: bool=False,
    extra_params: dict[str, float]={},
):
    """
    A binomial option pricing model for calculating stock prices, option values, and deltas.

    Parameters:
    option: OptionType - Enum representing the option type (Call, Put, etc.).
    n: int - Number of steps in the binomial model.
    S0: float - Initial stock price.
    u: float - Up movement factor.
    d: float - Down movement factor.
    K: float - Strike price.
    I: float - Interest rate.
    hist_dependent: bool - If the option is dependent on historical prices (e.g., Asian, Lookback).
    extra_params: dict - Additional parameters required for certain option types (e.g., power for power options).

    Returns:
    S: np.ndarray - The stock prices at each node.
    V: np.ndarray - The option values at each node.
    Delta: np.ndarray - The option delta at each node.
    """
    p = (1 + I - d) / (u - d)
    q = 1 - p

    if hist_dependent:
        S = np.zeros((2**n, n+1))
        combinations = list(itertools.product([u, d], repeat=n))
        for i in range(2**n):
            combination = [S0] + list(combinations[i])
            S[i, :] = np.cumprod(combination)

        payoff = np.array(
            [option.payoff(K, S[j, n], history=S[j, :]) for j in range(2**n)]
        ).reshape(-1, 1)

        V = np.zeros((2**n, n+1))
        V[:, n] = payoff.flatten()
        for j in range(n-1,-1,-1):
            for h in range(0, 2**n, 2**(n-j)):
                V[h, j] = discount(p*V[h,j+1] + q*V[h+2**(n-j-1),j+1], I)

        Delta = np.zeros((2**(n-1), n))
        for h in range(n):
            for j in range(0, 2**(n-1), 2**(n-h-1)):
                Delta[j,h] = (
                    (V[2*j,h+1] - V[2*j+2**(n-h-1),h+1]) /
                    (S[2*j,h+1] - S[2*j+2**(n-h-1),h+1])
                )

    else:
        S = np.zeros((n+1, n+1))
        for h in range(n+1):
            for j in range(h+1):
                S[j,h] = S0 * u**(h-j) * d**j

        payoff = np.array(
            [option.payoff(K, S[j, n], **extra_params) for j in range(n+1)]
        ).reshape(-1, 1)

        V = np.zeros((n+1, n+1))
        V[:, n] = payoff.flatten()
        for j in range(n-1,-1,-1):
            for h in range(j+1):
                V[h,j] = discount(p*V[h,j+1] + q*V[h+1,j+1], I)

        Delta = np.zeros((n, n))
        for h in range(n):
            for j in range(h+1):
                Delta[j,h] = (V[j,h+1] - V[j+1,h+1]) / (S[j,h+1] - S[j+1,h+1])

    return S, V, Delta

option = OptionType.Call
n = 4
S0 = 50
u = 1.2
d = 0.9
K = 45
I = 0.05
extra_params = {'power': 2}
S, V, Delta = binomial(option, n, S0, u, d, K, I, extra_params)

S = pretty_table(S, n+1, 'S')
V = pretty_table(V, n+1, 'V')
Delta = pretty_table(Delta, n, 'Delta')

print(S)
print(V)