'''
Created on Jul 25, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

from jmetal.util.sched_utils import bmta, maxmin_core
from jmetal.problem.multiobjective.constrained import Schedule
from jmetal.core.algorithm import Algorithm
from jmetal.util import machine

import time

class BMFMMS(Algorithm[None,None]):
    '''
    Balanced Makespan First, Max-Min Second algorithm: Simple deterministic algorithm to schedule independent \
    tasks over heterogeneous (virtual) machines. The BMFMMS applies the Balanced Makespan Task Allocation (BMTA) \
    algorithm in the first phase, then the Max-Min Task Allocation second.
    '''

    def __init__(self, problem: Schedule):
        '''
        The algorithm expects a SCHEDULE problem
        '''
        
        super().__init__()
        self.problem=problem
        self.machin=self.problem.getMachines()  # Retrieve list of machines from input scheduling problem
        self.tin=self.problem.getTasks()        # Retrieve list of tasks from input scheduling problem
        
    def run(self,ds_id:int=None,iteration:int=None)->dict:
        '''
        @param ds_id: Dataset ID 
        @type ds_id: int
        @param iteration: Iteration number 
        @type iteration: int 
        @return: Run time results for the algorithm, as well as updated machines' status (e.g., makespan, assignment of tasks to different machines, ... etc)
        @rtype: Dictionary
        '''
        
        # Record running time of BMFMMS
        self.start_computing_time = time.time()
        maxmin_core(self.machin, bmta(self.machin, self.tin))
        self.total_computing_time = self.get_current_computing_time()
        runtime_res={'algorithm':'BMFMMS','ds_id':ds_id,'iteration':iteration,'start':self.start_computing_time,'end':self.start_computing_time+self.total_computing_time,\
                'total_time':self.total_computing_time,'max_makespan':machine.getMachMaxMakespan(self.machin).makespan}
        
        # Record machines' assigned tasks, makespan and any other required properties 
        m_res=[]
        for m in self.machin:
            m_res.append({'algorithm':'BMFMMS','ds_id':ds_id,'iteration':iteration,'machine_id':m.id,'tasks':\
                      [t.id for t in m.tasks],'makespan':m.makespan})
        
        # Reset machines
        machine.resetMachines(self.machin)
        
        # Return final results
        fin_res={}
        fin_res['run_time']=runtime_res
        fin_res['mach_res']=m_res
        return fin_res
        
        