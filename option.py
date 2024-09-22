from abc import ABC, abstractmethod
from enum import Enum
from utils import PositionType

import numpy as np

class OptionType(Enum):
    CALL = "call"
    PUT = "put"

class BarrierType(Enum):
    UP_AND_OUT = "up and out"
    DOWN_AND_OUT = "down and out"
    UP_AND_IN = "up and in"
    DOWN_AND_IN = "down and in"

TRAJECTORY_DEPENDENT_CLASSES = ['LookbackOption', 'AsianOption', 'BarrierOption']

class Option(ABC):
    def __init__(
        self,
        type: str,
        K: float,
        T: float,
        premium: float = 0,
        position: PositionType = PositionType.LONG,
        **kwargs
    ):
        if isinstance(type, str):
            try:
                self.type = OptionType(type.lower())
            except ValueError:
                raise ValueError(f"Invalid option type '{type}'. Must be 'call' or 'put'.")
        else:
            raise ValueError("Option type should be provided as a string ('call' or 'put').")
        if not isinstance(position, PositionType):
            raise ValueError("Invalid position type. It should be either 'long' or 'short'")
        self.K = K
        self.T = T
        self.premium = premium
        self.position = position
        self.name = self.__class__.__name__
        self._is_trajectory_dependent = self.name in TRAJECTORY_DEPENDENT_CLASSES

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return (f"{self.name}, {self.type.value}, {self.position.value}, "
                f"K={self.K}, T={self.T}")

    def __repr__(self):
        return (f"{self.name}, {self.type.value}, {self.position.value}, "
                f"K={self.K}, T={self.T}")

    @property
    def is_trajectory_dependent(self):
        return self._is_trajectory_dependent

    @abstractmethod
    def payoff(self, S_T, **kwargs):
        pass

    def revenue(self, S_T, **kwargs):
        if self.position == PositionType.LONG:
            return self.payoff(S_T, **kwargs) - self.premium
        else:
            return self.payoff(S_T, **kwargs) + self.premium


class VanillaOption(Option):
    def payoff(self, S_T):
        if self.type == OptionType.CALL:
            base_payoff = max(S_T - self.K, 0)
        else:
            base_payoff = max(self.K - S_T, 0)
        return base_payoff if self.position == PositionType.LONG else -base_payoff

class BinaryOption(Option):
    def payoff(self, S_T):
        if self.type == OptionType.CALL:
            return self.B if S_T > self.K else 0
        else:
            return self.B if S_T < self.K else 0

class PowerOption(Option):
    def payoff(self, S_T):
        if self.type == OptionType.CALL:
            return max(S_T - self.K, 0)**self.power
        else:
            return max(self.K - S_T, 0)**self.power

class LookbackOption(Option):
    def payoff(self, S_T, trajectory):
        if self.type == OptionType.CALL:
            return S_T - min(trajectory)
        else:
            return max(trajectory) - S_T

class AsianOption(Option):
    def payoff(self, S_T, trajectory):
        if self.type == OptionType.CALL:
            return max(np.mean(trajectory) - self.K, 0)
        else:
            return max(self.K - np.mean(trajectory), 0)

class BarrierOption(Option):
    def payoff(self, S_T, trajectory):
        if self.type == OptionType.CALL:
            if self.barrier_type == BarrierType.UP_AND_OUT:
                return 0 if any(trajectory > self.B) else max(S_T - self.K, 0)
            elif self.barrier_type == BarrierType.DOWN_AND_OUT:
                return 0 if any(trajectory < self.B) else max(S_T - self.K, 0)
            elif self.barrier_type == BarrierType.UP_AND_IN:
                return 0 if all(trajectory > self.B) else max(S_T - self.K, 0)
            elif self.barrier_type == BarrierType.DOWN_AND_IN:
                return 0 if all(trajectory < self.B) else max(S_T - self.K, 0)
        else:
            if self.barrier_type == BarrierType.UP_AND_OUT:
                return 0 if any(trajectory > self.B) else max(self.K - S_T, 0)
            elif self.barrier_type == BarrierType.DOWN_AND_OUT:
                return 0 if any(trajectory < self.B) else max(self.K - S_T, 0)
            elif self.barrier_type == BarrierType.UP_AND_IN:
                return 0 if all(trajectory > self.B) else max(self.K - S_T, 0)
            elif self.barrier_type == BarrierType.DOWN_AND_IN:
                return 0 if all(trajectory < self.B) else max(self.K - S_T, 0)

# class DoubleBarrierOption(Option):
#     def __init__(self, type: OptionType, K: float, T: float, B1: float, B2: float):
#         super().__init__(type, K, T)
#         self.B1 = B1
#         self.B2 = B2

#     def payoff(self, S_T, **kwargs):
#         pass

#     def payoff_double_barrier_call(K, S_T, **kwargs):
#         B1 = kwargs['B1']
#         B2 = kwargs['B2']
#         hist = kwargs['history']
#         return 0 if any(hist > B2) or any(hist < B1) else OptionType.payoff_call(K, S_T)

#     @staticmethod
#     def payoff_double_barrier_put(K, S_T, **kwargs):
#         B1 = kwargs['B1']
#         B2 = kwargs['B2']
#         hist = kwargs['history']
#         return 0 if any(hist > B2) or any(hist < B1) else OptionType.payoff_put(K, S_T)
