import numpy as np

from option_type import OptionType, HIST_DEPENDENT
from utils import *

def binomial(
    option: OptionType,
    n: int,
    S0: float,
    u: float,
    d: float,
    K: float,
    I: float,
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
    extra_params: dict - Additional parameters required for certain option types (e.g., power for power options).

    Returns:
    S: np.ndarray - The stock prices at each node.
    V: np.ndarray - The option values at each node.
    Delta: np.ndarray - The option delta at each node.
    """
    p = (1 + I - d) / (u - d)
    q = 1 - p

    hist_dependent = option in HIST_DEPENDENT
    S = stock_prices(S0, u, d, n, hist_dependent)
    if hist_dependent:
        payoff = np.array(
            [option.payoff(K, S[j, n], history=S[j, :], **extra_params) for j in range(2**n)]
        ).reshape(-1, 1)
    else:
        payoff = np.array(
            [option.payoff(K, S[j, n], **extra_params) for j in range(n+1)]
        ).reshape(-1, 1)
    V = option_prices(p, q, I, payoff, n, hist_dependent)
    Delta = delta_coverage(S, V, n, hist_dependent)

    return S, V, Delta


option = OptionType.DoubleBarrierCall
n = 3
S0 = 20
u = 1.2
d = 0.95
K = 19
I = 0.03
extra_params = {'B1': 18, 'B2': 25}

S, V, Delta = binomial(option, n, S0, u, d, K, I, extra_params)

S = pretty_table(S, n+1, 'S')
V = pretty_table(V, n+1, 'V')
Delta = pretty_table(Delta, n, 'Delta')

print(S)
print(V)
print(Delta)