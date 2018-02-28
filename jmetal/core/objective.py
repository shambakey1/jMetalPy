
from jmetal.core.problem import Problem
from jmetal.core.solution import Solution

__author__ = "Antonio J. Nebro"


class Objective:
    def __init__(self,weight:float=1.0,thr:float=0.0):
        self.weight=weight  # Assign weight for current objective
        self.thr=thr        # Evaluation threshold difference between current and previous solution
        self.prev_solu_eval=float('inf')    # Holds the evaluation of previous solution
        self.cur_solu_eval=float('inf')     # Holds the evaluation of current solution
        
    def compute(self, solution: Solution, problem: Problem) -> float:
        pass

    def is_a_minimization_objective(self) -> bool:
        return True
    
