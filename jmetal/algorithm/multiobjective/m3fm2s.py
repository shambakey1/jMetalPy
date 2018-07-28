'''
Created on Jul 26, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

from jmetal.util.sched_utils import maxmin_core, maxmin_makespan_thr_core
from jmetal.problem.multiobjective.constrained import Schedule
from jmetal.core.algorithm import Algorithm
from jmetal.util import machine

import time

class M3FM2S(Algorithm[None,None]):
    '''
    Max-Min with Makespan threshold First, Max-Min Second algorithm: Simple deterministic algorithm to schedule independent \
    tasks over heterogeneous (virtual) machines. The M3FM2S applies the Max-Min with Makespan threshold \
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
        makespan_in=sum([i.length for i in self.tin])/sum([j.speed for j in self.machin])
        #maxmin_makespan_thr_core(self.machin, self.tin,makespan_in)
        maxmin_core(self.machin, self.tin,maxmin_makespan_thr_core(self.machin, self.tin,makespan_in))
        self.total_computing_time = self.get_current_computing_time()
        runtime_res={'algorithm':'M3FM2S','ds_id':ds_id,'iteration':iteration,'start':self.start_computing_time,'end':self.start_computing_time+self.total_computing_time,\
                'total_time':self.total_computing_time,'max_makespan':machine.getMachMaxMakespan(self.machin).makespan}
        
        # Record machines' assigned tasks, makespan and any other required properties 
        m_res=[]
        for m in self.machin:
            m_res.append({'algorithm':'M3FM2S','ds_id':ds_id,'iteration':iteration,'machine_id':m.id,'tasks':\
                      [t.id for t in m.tasks],'makespan':m.makespan})
        
        # Reset machines
        machine.resetMachines(self.machin)
        
        # Return final results
        fin_res={}
        fin_res['run_time']=runtime_res
        fin_res['mach_res']=m_res
        return fin_res
        
        