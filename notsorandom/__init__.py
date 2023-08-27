from bisect import bisect
from itertools import accumulate
from random import Random
from typing import Any, List, Tuple, TypedDict

__version__ = "0.0.1"


class NotSoRandomState(TypedDict):
    r: Tuple[Any, ...]
    super: Tuple[Any, ...]
    intervals: int
    weights: List[int]
    delta: float


class NotSoRandom(Random):
    def __init__(self, x: Any = None, n: int = 10) -> None:
        super().__init__(x)
        self._r = Random()
        self.intervals: int = 2**n
        self.weights: List = [1] * self.intervals
        self.delta = 1 / self.intervals
        self.valid = [0] * self.intervals

    def random(self) -> float:
        rand = self._r.random()
        src_interval = int(rand // self.delta)
        dst_interval = self.argchoice(self.weights, rand=rand)

        fudge = rand + ((dst_interval - src_interval) * self.delta)

        for i in range(0, self.intervals):
            self.weights[i] += 1
        self.weights[dst_interval] = 1

        return fudge

    def argchoice(self, weights: List[int] = [], rand=None):
        sum_weights = list(accumulate(weights))
        total = float(sum_weights[-1])
        return bisect(sum_weights, (rand or self._r.random()) * total, 0, len(weights) - 1)

    def getstate(self):
        return NotSoRandomState(
            r=self._r.getstate(),
            super=super().getstate(),
            intervals=self.intervals,
            weights=self.weights,
            delta=self.delta,
        )

    def setstate(self, state: NotSoRandomState) -> None:
        super().setstate(state["super"])
        self._r.setstate(state["r"])
        self.intervals = state["intervals"]
        self.weights = state["weights"]
        self.delta = state["delta"]
