from multiprocessing.pool import ThreadPool
from typing import TypeVar, List, Generic

from jmetal.core.problem import Problem

S = TypeVar('S')


class Evaluator(Generic[S]):
    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        pass

    @staticmethod
    def evaluate_solution(solution: S, problem: Problem) -> None:
        problem.evaluate(solution)
        if problem.number_of_constraints > 0:
            problem.evaluate_constraints(solution)


class SequentialEvaluator(Evaluator[S]):
    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        for solution in solution_list:
            Evaluator.evaluate_solution(solution, problem)

        return solution_list


class ParallelEvaluator(Evaluator[S]):
    def __init__(self, processes=None):
        self.pool = ThreadPool(processes)

    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        self.pool.map(lambda solution: Evaluator[S].evaluate_solution(solution, problem), solution_list)

        return solution_list
