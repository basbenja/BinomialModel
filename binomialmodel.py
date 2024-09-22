import numpy as np

from option import Option
from utils import *

def binomial(
    option: Option,
    S0: float,
    u: float,
    d: float,
    I: float,
):
    """
    A binomial option pricing model for calculating stock prices, option values,
    and deltas.

    Parameters:
    option: Option - Class representing the option.
    S0: float - Initial stock price.
    u: float - Up movement factor.
    d: float - Down movement factor.
    I: float - Interest rate.

    Returns:
    S: np.ndarray - The stock prices at each node.
    V: np.ndarray - The option values at each node.
    Delta: np.ndarray - The option delta at each node.
    """
    p = (1 + I - d) / (u - d)
    q = 1 - p

    is_trajectory_dependent = option.is_trajectory_dependent
    T = option.T
    S = stock_prices(S0, u, d, T, is_trajectory_dependent)
    if is_trajectory_dependent:
        payoff = np.array(
            [option.payoff(S_T=S[j, T], trajectory=S[j, :]) for j in range(2**T)]
        ).reshape(-1, 1)
    else:
        payoff = np.array(
            [option.payoff(S_T=S[j, T]) for j in range(T+1)]
        ).reshape(-1, 1)
    V = option_prices(p, q, I, payoff, T, is_trajectory_dependent)
    Delta = delta_coverage(S, V, T, is_trajectory_dependent)

    return S, V, Delta