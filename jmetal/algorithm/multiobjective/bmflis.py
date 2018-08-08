'''
Created on Jan 18, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

from jmetal.util.sched_utils import bmta, lmita, redTasks, maxmin_core
from jmetal.problem.multiobjective.constrained import Schedule
from jmetal.core.algorithm import Algorithm
from jmetal.util import machine

import time

class BMFLIS(Algorithm[None,None]):
    '''
    Balanced Makespan First, Least-Increase Second algorithm with re-assignment: Simple deterministic algorithm to schedule independent \
    tasks over heterogeneous (virtual) machines. The BMFLIS applies the Balanced Makespan Task Allocation (BMTA) \
    algorithm in the first phase, then the Least Makespan-Increase Task Allocation (LMITA) second. Finally, tasks 
    are re-assigned from the machine with maximum makespan if this is going to reduce the makespan with better 
    resource utilization
    '''

    def __init__(self, problem: Schedule):
        '''
        The algorithm expects a SCHEDULE problem
        '''
        
        super().__init__()
        self.problem=problem
        self.machin=self.problem.getMachines()  # Retrieve list of machines from input scheduling problem
        self.tin=self.problem.getTasks()        # Retrieve list of tasks from input scheduling problem
        
    def run(self,ds_id:int=None,iteration:int=None,th_per:float=0.0)->dict:
        '''
        @param ds_id: Dataset ID 
        @type ds_id: int
        @param iteration: Iteration number 
        @type iteration: int 
        @param th_per: Threshold percentage that should be added over the theoretical bound on makespan to allow for more tasks to be assigned to each machine
        @type th_per: float
        @return: Run time results for the algorithm, as well as updated machines' status (e.g., makespan, assignment of tasks to different machines, ... etc)
        @rtype: Dictionary
        '''
        
        # Record running time of BMFLIS
        self.start_computing_time = time.time()
        if len(self.tin)<=len(self.machin): # Apply MAXMIN in case number of tasks is less than number of machines
            maxmin_core(self.machin,self.tin)
        else:
            lmita(self.machin, bmta(self.machin, self.tin,th_per=th_per))
            redTasks(self.machin,self.tin)
        self.total_computing_time = self.get_current_computing_time()
        runtime_res={'algorithm':'BMFLIS','ds_id':ds_id,'iteration':iteration,'start':self.start_computing_time,'end':self.start_computing_time+self.total_computing_time,\
				'total_time':self.total_computing_time,'max_makespan':machine.getMachMaxMakespan(self.machin).makespan}
        
        # Record machines' assigned tasks, makespan and any other required properties 
        m_res=[]
        for m in self.machin:
            m_res.append({'algorithm':'BMFLIS','ds_id':ds_id,'iteration':iteration,'machine_id':m.id,'tasks':\
                      [t.id for t in m.tasks],'makespan':m.makespan})
        
        # Reset machines
        machine.resetMachines(self.machin)
        
        # Return final results
        fin_res={}
        fin_res['run_time']=runtime_res
        fin_res['mach_res']=m_res
        return fin_res
        
        