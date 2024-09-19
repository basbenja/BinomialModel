from enum import Enum
import numpy as np

class OptionType(Enum):
    Call = "call"
    Put = "put"
    BinaryCall = "binary_call"
    BinaryPut = "binary_put"
    PowerCall = "power_call"
    PowerPut = "power_put"
    LookbackCall = "lookback_call"
    LookbackPut = "lookback_put"
    AsianCall = "asian_call"
    AsianPut = "asian_put"
    BarrierCall = "barrier_call"
    BarrierPut = "barrier_put"

    @staticmethod
    def payoff_call(K, St, **kwargs):
        return max(St - K, 0)

    @staticmethod
    def payoff_put(K, St, **kwargs):
        return max(K - St, 0)

    @staticmethod
    def payoff_binary_call(K, St, **kwargs):
        B = kwargs['B']
        return B if St > K else 0

    @staticmethod
    def payoff_binary_put(K, St, **kwargs):
        B = kwargs['B']
        return B if St < K else 0

    @staticmethod
    def payoff_power_call(K, St, **kwargs):
        p = kwargs['power']
        return max(St - K, 0)**p

    @staticmethod
    def payoff_power_put(K, St, **kwargs):
        p = kwargs['power']
        return max(K - St, 0)**p

    @staticmethod
    def payoff_lookback_call(K, St, **kwargs):
        hist = kwargs['history']
        return St - min(hist)

    @staticmethod
    def payoff_lookback_put(K, St, **kwargs):
        hist = kwargs['history']
        return max(hist) - St

    @staticmethod
    def payoff_asian_call(K, St, **kwargs):
        hist = kwargs['history']
        return max(np.mean(hist) - K, 0)

    @staticmethod
    def payoff_asian_put(K, St, **kwargs):
        hist = kwargs['history']
        return max(K - np.mean(hist), 0)

    @staticmethod
    def payoff_barrier_call(K, St, **kwargs):
        B = kwargs['B']
        hist = kwargs['history']
        type = kwargs['type']
        if type == "up and out":
            return 0 if any(hist > B) else OptionType.payoff_call(K, St)
        elif type == "down and out":
            return 0 if any(hist < B) else OptionType.payoff_call(K, St)

    @staticmethod
    def payoff_barrier_put(K, St, **kwargs):
        B = kwargs['B']
        hist = kwargs['history']
        type = kwargs['type']
        if type == "up and out":
            return 0 if any(hist > B) else OptionType.payoff_put(K, St)
        elif type == "down and out":
            return 0 if any(hist < B) else OptionType.payoff_put(K, St)

    def payoff(self, K, St, **kwargs):
        match self:
            case OptionType.Call:
                return self.payoff_call(K, St, **kwargs)
            case OptionType.Put:
                return self.payoff_put(K, St, **kwargs)
            case OptionType.BinaryCall:
                return self.payoff_binary_call(K, St, **kwargs)
            case OptionType.BinaryPut:
                return self.payoff_binary_put(K, St, **kwargs)
            case OptionType.PowerCall:
                return self.payoff_power_call(K, St, **kwargs)
            case OptionType.PowerPut:
                return self.payoff_power_put(K, St, **kwargs)
            case OptionType.LookbackCall:
                return self.payoff_lookback_call(K, St, **kwargs)
            case OptionType.LookbackPut:
                return self.payoff_lookback_put(K, St, **kwargs)
            case OptionType.AsianCall:
                return self.payoff_asian_call(K, St, **kwargs)
            case OptionType.AsianPut:
                return self.payoff_asian_put(K, St, **kwargs)
            case OptionType.BarrierCall:
                return self.payoff_barrier_call(K, St, **kwargs)
            case OptionType.BarrierPut:
                return self.payoff_barrier_put(K, St, **kwargs)
            case _:
                raise ValueError(f"Unknown option type: {self}")
