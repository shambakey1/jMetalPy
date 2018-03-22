'''
Created on Jan 18, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

from jmetal.util.sched_utils import bmta, lmita
from jmetal.problem.multiobjective.constrained import Schedule
from jmetal.core.algorithm import Algorithm
import time

class BMFLIS(Algorithm[None,None]):
    '''
    Balanced Makespan First, Least-Increase Second algorithm: Simple deterministic algorithm to schedule independent \
    tasks over heterogeneous (virtual) machines. The BMFLIS applies the Balanced Makespan Task Allocation (BMTA) \
    algorithm in the first phase, then the Least Makespan-Increase Task Allocation (LMITA) second.
    '''

    def __init__(self, problem: Schedule):
        '''
        The algorithm expects a SCHEDULE problem
        '''
        super().__init__()
        self.problem=problem
        self.machin=self.problem.getMachines()  # Retrieve list of machines from input scheduling problem
        self.tin=self.problem.getTasks()        # Retrieve list of tasks from input scheduling problem
        
    def run(self)->None:
        self.start_computing_time = time.time()
        lmita(self.machin, bmta(self.machin, self.tin))
        self.total_computing_time = self.get_current_computing_time()
        results={'start':self.start_computing_time,'end':self.start_computing_time+self.total_computing_time,\
				'total_time':self.total_computing_time}
        print('start: '+str(self.start_computing_time)+', end: '+str(self.start_computing_time+self.total_computing_time)+', total: '+str(self.total_computing_time))
        
        