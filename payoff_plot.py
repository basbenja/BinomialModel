import numpy as np
import matplotlib.pyplot as plt

from option import *


######### Por ahora solo va a andar con opciones que no dependan de la trayectoria
def payoff_plot(strategy: list[Option]):
    max_K = max([option.K for option in strategy])
    S_T = np.linspace(0, 2*max_K, 100)

    total_payoff = np.zeros_like(S_T)
    for option in strategy:
        payoff = np.array([option.payoff(s) for s in S_T])
        plt.plot(S_T, payoff, label=str(option), linestyle="--")
        total_payoff += payoff

    plt.plot(S_T, total_payoff)
    plt.xlabel("Stock Price at Maturity $S(T)$")
    plt.ylabel("Payoff")
    plt.legend()
    plt.grid()
    plt.show()

strategy = [VanillaOption(OptionType.CALL, 100, 5), VanillaOption(OptionType.PUT, 100, 5)]
payoff_plot(strategy)