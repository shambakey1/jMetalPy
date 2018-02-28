from math import pi, cos, atan

""" Unconstrained Test problems for multi-objective optimization """
from jmetal.core.objective import Objective
from jmetal.core.solution import FloatSolution

from jmetal.core.problem import FloatProblem
from builtins import str
from typing import List
from _ast import Str
from jmetal.util.machine import Machine
from jmetal.util.task import Task
from jmetal.util import machine


class Srinivas(FloatProblem):
    """ Class representing problem Srinivas """
    def __init__(self):
        self.objectives = [self.Objective1(), self.Objective2()]

        self.number_of_objectives = len(self.objectives)
        self.number_of_variables = 2
        self.number_of_constraints = 2

        self.lower_bound = [-20.0 for i in range(self.number_of_variables)]
        self.upper_bound = [20.0 for i in range(self.number_of_variables)]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def get_name(self):
        return "Srinivas"

    class Objective1(Objective):
        def compute(self, solution: FloatSolution, problem: FloatProblem):
            x1 = solution.variables[0]
            x2 = solution.variables[1]

            return 2.0 + (x1 - 2.0) * (x1 - 2.0) + (x2 - 1.0) * (x2 - 1.0)

    class Objective2(Objective):
        def compute(self, solution: FloatSolution, problem: FloatProblem):
            x1 = solution.variables[0]
            x2 = solution.variables[1]

            return 9.0 * x1 - (x2 - 1.0) * (x2 - 1.0)

    def evaluate_constraints(self, solution: FloatSolution) -> None:
        constraints : [float] = [0.0 for x in range(self.number_of_constraints)]

        x1 = solution.variables[0]
        x2 = solution.variables[1]

        constraints[0] = 1.0 - (x1 * x1 + x2 * x2) / 225.0
        constraints[1] = (3.0 * x2 - x1) / 10.0 - 1.0

        overall_constraint_violation = 0.0
        number_of_violated_constraints = 0.0

        for constrain in constraints:
            if constrain < 0.0:
                overall_constraint_violation += constrain
                number_of_violated_constraints += 1

        solution.attributes["overall_constraint_violation"] = overall_constraint_violation
        solution.attributes["number_of_violated_constraints"] = number_of_violated_constraints


class Tanaka(FloatProblem):
    """ Class representing problem Tanaka """
    def __init__(self):
        self.objectives = [self.Objective1(), self.Objective2()]

        self.number_of_objectives = len(self.objectives)
        self.number_of_variables = 2
        self.number_of_constraints = 2

        self.lower_bound = [10e-5 for i in range(self.number_of_variables)]
        self.upper_bound = [pi for i in range(self.number_of_variables)]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def get_name(self):
        return "Tanaka"

    class Objective1(Objective):
        def compute(self, solution: FloatSolution, problem: FloatProblem):
            return solution.variables[0]

    class Objective2(Objective):
        def compute(self, solution: FloatSolution, problem: FloatProblem):
            return solution.variables[1]

    def evaluate_constraints(self, solution: FloatSolution) -> None:
        constraints : [float] = [0.0 for x in range(self.number_of_constraints)]

        x1 = solution.variables[0]
        x2 = solution.variables[1]

        constraints[0] = (x1 * x1 + x2 * x2 - 1.0 - 0.1 * cos(16.0 * atan(x1 / x2)))
        constraints[1] = -2.0 * ((x1 - 0.5) * (x1 - 0.5) + (x2 - 0.5) * (x2 - 0.5) - 0.5)

        overall_constraint_violation = 0.0
        number_of_violated_constraints = 0.0

        for constrain in constraints:
            if constrain < 0.0:
                overall_constraint_violation += constrain
                number_of_violated_constraints += 1

        solution.attributes["overall_constraint_violation"] = overall_constraint_violation
        solution.attributes["number_of_violated_constraints"] = number_of_violated_constraints

class Schedule(FloatProblem):
    ''' Task scheduling problem on heterogeneous (virtual) machines. Current objectives include subset or all of \\
    makespan, cost and energy. Cost per time unit for each machine is fixed. Each scheduling variable corresponds to \\
    a machine. Each variable value is total lengths of tasks allocated to this machine divided by the speed of the \\
    the machine. Current objectives (i.e., makespan, cost and energy) are directly proportional to variables values.
    Different variations of the problem include:
    1- Independent tasks scheduling    
    '''
    def __init__(self,objs:List[dict],machin:List[Machine],tin:List[Task],consts:List[str]=[]):
        '''
        @param objs: List of scheduling objectives as dictionaries. Each dictionary consists of a name (e.g, makespan, cost, energy), and a weight for the objective
        @type objs: List[tuple] 
        @param machin: Set of machines
        @type machin: List[Machine]
        @param tin: List of (independent) tasks
        @type tin: List[Task]   
        @param consts: List of constraints 
        @type consts: List[str] 
        ''' 
        
        self.objectives=[]  # Initialize an empty set of objectives for the scheduling problem
        self.machin=machin  # List of machines
        self.tin=tin        # List of tasks
        
        # Define required scheduling objective(s) with weight(s) for each objective if any
        for obj in objs:
            if obj['name'].lower()=='makespan': # If makespan is an objective, then add makespan to list of objectives
                self.objectives.append(self.ObjectiveMakespan(obj['weight']))
            elif obj['name'].lower()=='cost':  # If cost is an objective, then add cost to list of objectives
                self.objectives.append(self.ObjectiveCost(obj['weight']))
            elif obj['name'].lower()=='energy':   # If energy is an objective, then add energy to list of objectives
                self.objectives.append(self.ObjectiveEnergy(obj['weight']))

        self.number_of_objectives = len(self.objectives)
        self.number_of_variables = len(self.machin) # Current implementation consider machines as scheduling variables
        self.number_of_constraints = len(self.consts)   #TODO: Currently, there are no constraints
        
        # Define lower and upper limits according to objectives
        self.lower_bound = [0.0 for i in range(self.number_of_variables)]
        t_len=sum(t.length for t in tin)    # Total length of all tasks
        self.upper_bound = [t_len/m.speed for i in range(self.number_of_variables) for m in machin if m.id==i]  # Upper bound when all tasks are assigned to each machine
        '''
        for i in range(self.number_of_variables):   #TODO: Current implementation assumes weighted objectives to calculate upper limit for each variable. Other implementations may require other calculation ways
            m=next(m_req for m_req in machin if m_req.id==i)    # Retrieve next machine that corresponds to current variable
            self.upper_bound[i]+=sum(t.length for t in self.tin)/m.speed
            for obj in objs:
                if obj['name'].lower()=='makespan':
                    self.upper_bound[i]+=sum(t.length for t in self.tin)/m.speed*obj['weight']
                elif obj['name'].lower()=='cost':
                    self.upper_bound[i]+=sum(t.length for t in self.tin)/m.speed*m.cost*obj['weight']   # Assuming fixed time unit cost per machine
                elif obj['name'].lower()=='energy':
                    continue    #FIXME: To be implemented  
        '''
        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def get_name(self):
        return "Schedule"
    
    def getMachines(self):
        ''' Return machines list '''
        
        return self.machin
    
    def getTasks(self):
        ''' Return tasks list '''
        
        return self.tin

    class ObjectiveMakespan(Objective):
        ''' Minimum makespan objective ''' 
        
        def __init__(self,weight:float=1.0):
            super.__init__()
            self.weight=weight  # Assign weight for current objective
            
        def compute(self, solution: FloatSolution, problem: FloatProblem):
            return max(solution.variables)*self.weight

    class ObjectiveCost(Objective):
        ''' Minumum cost objective '''
        
        def __init__(self,machin:List[Machine], weight:float=1.0):
            super.__init__()
            self.machin=machin
            self.weight=weight  # Assign weight for current objective
            
        def compute(self, solution: FloatSolution, problem: FloatProblem):
            return sum(m.cost*solution.variables[i] for i in range(self.number_of_variables) for m in self.machin if m.id==i)
    
    class ObjectiveEnergy(Objective):
        ''' Minimum energy objective '''
        
        def __init__(self,weight:float=1.0):
            super.__init__()
            self.weight=weight  # Assign weight for current objective
            
        def compute(self, solution:FloatSolution, problem:FloatProblem)->float:
            return 0.0  #FIXME: Modify energy objective implementation
         

    def evaluate_constraints(self, solution: FloatSolution) -> None:
        pass

