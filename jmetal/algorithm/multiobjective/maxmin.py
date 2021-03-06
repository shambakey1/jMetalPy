'''
Created on Jul 23, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

from jmetal.problem.multiobjective.constrained import Schedule
from jmetal.core.algorithm import Algorithm
from jmetal.util import machine
from jmetal.util.sched_utils import maxmin_core

import time, sys

class MAXMIN(Algorithm[None,None]):
    '''
    MAXMIN scheduling algorithm to minimize makespan
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
        
        # Record running time of MINMIN
        self.start_computing_time = time.time()
        
        # Run the core of the maxmin algorithm
        maxmin_core(self.machin,self.tin)

        # Record end of MINMIN running time
        self.total_computing_time = self.get_current_computing_time()
        runtime_res={'algorithm':'MAXMIN','ds_id':ds_id,'iteration':iteration,'start':self.start_computing_time,'end':self.start_computing_time+self.total_computing_time,\
                'total_time':self.total_computing_time,'max_makespan':machine.getMachMaxMakespan(self.machin).makespan}
        
        # Record machines' assigned tasks, makespan and any other required properties 
        m_res=[]
        for m in self.machin:
            m_res.append({'algorithm':'MAXMIN','ds_id':ds_id,'iteration':iteration,'machine_id':m.id,'tasks':\
                      [t.id for t in m.tasks],'makespan':m.makespan})
        
        # Reset machines
        machine.resetMachines(self.machin)
        
        # Return final results
        fin_res={}
        fin_res['run_time']=runtime_res
        fin_res['mach_res']=m_res
        return fin_res
        
        