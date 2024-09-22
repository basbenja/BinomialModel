import numpy as np
import matplotlib.pyplot as plt

from option import *
from stock import *

######### Por ahora solo va a andar con opciones que no dependan de la trayectoria
def payoff_plot(portfolio: list[Option], revenue: bool = False):
    max_K = max([option.K for option in portfolio if isinstance(option, Option)])
    S_T = np.linspace(0, 2*max_K, 100)

    total = np.zeros_like(S_T)
    for asset in portfolio:
        if revenue:
            rev = np.array([asset.revenue(s) for s in S_T])
            plt.plot(S_T, rev, label=str(asset), linestyle="--")
            total += rev
        else:
            payoff = np.array([asset.payoff(s) for s in S_T])
            plt.plot(S_T, payoff, label=str(asset), linestyle="--")
            total += payoff

    label = "revenue" if revenue else "payoff"
    plt.plot(S_T, total, label=f"Total {label}", linewidth=3)
    plt.xlabel("Stock Price at Maturity $S(T)$")
    plt.axhline(0, color="black", linewidth=2)
    plt.axvline(0, color="black", linewidth=2)
    plt.ylabel(label.capitalize())
    plt.legend()
    plt.grid()
    plt.show()

# portfolio = [
#     VanillaOption(type="call", K=100, T=5, position=PositionType.LONG),
#     VanillaOption(type="call", K=160, T=5, position=PositionType.LONG),
#     VanillaOption(type="call", K=130, T=5, position=PositionType.SHORT),
#     VanillaOption(type="call", K=130, T=5, position=PositionType.SHORT),
# ]
