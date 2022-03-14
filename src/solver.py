from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from docplex.mp.model import *
from docplex.mp.solution import SolveSolution

from config import Config


@dataclass
class Solution:
    objective_value: float


class Solver:
    def __init__(self, config: Config):
        self.config = config
        self.model = Model()
        self.build_instance()

    def build_instance(self):
        # set up variables
        self.example_var = self.model.continuous_var(0, 1)

    def solve(self) -> Solution:
        self.model.maximize(self.example_var)
        solution = self.model.solve()
        if solution is None:
            return None
        return Solution(solution.get_objective_value())

    @staticmethod
    def from_file(f) -> Solver:
        config = Config.load(f)
        return Solver(config)
