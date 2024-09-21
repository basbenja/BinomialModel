import itertools
import numpy as np

from tabulate import tabulate

def stock_prices(S0, u, d, n, hist_dependent=False):
    if hist_dependent:
        S = np.zeros((2**n, n+1))
        combinations = list(itertools.product([u, d], repeat=n))
        for i in range(2**n):
            combination = [S0] + list(combinations[i])
            S[i, :] = np.cumprod(combination)
    else:
        S = np.zeros((n+1, n+1))
        for h in range(n+1):
            for j in range(h+1):
                S[j,h] = S0 * u**(h-j) * d**j
    return S


def option_prices(p, q, I, payoff, n, hist_dependent=False):
    if hist_dependent:
        V = np.zeros((2**n, n+1))
        V[:, n] = payoff.flatten()
        for j in range(n-1,-1,-1):
            for h in range(0, 2**n, 2**(n-j)):
                V[h, j] = discount(p*V[h,j+1] + q*V[h+2**(n-j-1),j+1], I)
    else:
        V = np.zeros((n+1, n+1))
        V[:, n] = payoff.flatten()
        for j in range(n-1,-1,-1):
            for h in range(j+1):
                V[h,j] = discount(p*V[h,j+1] + q*V[h+1,j+1], I)
    return V


def delta_coverage(S, V, n, hist_dependent=False):
    if hist_dependent:
        Delta = np.zeros((2**(n-1), n))
        for h in range(n):
            for j in range(0, 2**(n-1), 2**(n-h-1)):
                Delta[j,h] = (
                    (V[2*j,h+1] - V[2*j+2**(n-h-1),h+1]) /
                    (S[2*j,h+1] - S[2*j+2**(n-h-1),h+1])
                )
    else:
        Delta = np.zeros((n, n))
        for h in range(n):
            for j in range(h+1):
                Delta[j,h] = (V[j,h+1] - V[j+1,h+1]) / (S[j,h+1] - S[j+1,h+1])
    return Delta


def discount(value, i, T=1):
    return value / (1+i)**T


def pretty_table(array, n, process):
    return tabulate(
        np.round(array, 5),
        headers=[f"{process}_t={t}" for t in range(n)],
        tablefmt="mixed_grid",
        numalign="center",
        stralign="center"
    )