import numpy as np
from tabulate import tabulate

discount = lambda value, i, T=1: value / (1+i)**T

def pretty_table(array, n, process):
    return tabulate(
        np.round(array, 5),
        headers=[f"{process}_t={t}" for t in range(n)],
        tablefmt="mixed_grid",
        numalign="center",
        stralign="center"
    )