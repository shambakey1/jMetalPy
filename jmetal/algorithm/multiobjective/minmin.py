'''
Created on Jul 21, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

from jmetal.problem.multiobjective.constrained import Schedule
from jmetal.core.algorithm import Algorithm
from jmetal.util import machine

import time, sys

class MINMIN(Algorithm[None,None]):
    '''
    MINMIN scheduling algorithm to minimize makespan
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
        
        # Calculate the initial completion time matrix of all tasks over all machines
        ct=[[j.makespan+i.length/j.speed for j in self.machin] for i in self.tin]
        
        # Temporary counter to hold number of tasks that has been assigned to machines
        tmp_cnt=len(ct)
        
        # Repeat until all tasks are assigned
        while tmp_cnt!=0:
            # Assign task with minimum completion time to the machine that causes this minimum completion time
            job_min=-1       # Job index with minimum completion time (initialized to -1 which corresponds to no task)
            machine_min=-1   # Machine index with minimum completion time (initialized to -1 which corresponds to no machine)
            tmp_mach_at_inc=sys.float_info.max    # Current increase in machine makespan (i.e., availability time) (initialized to maximum float value)
            
            # Traverse all completion time matrix to find the job with minimum completion time
            for job_no in range(len(ct)):
                if not self.tin[job_no].m:
                    for machine_no in range(len(ct[0])):
                        if ct[job_no][machine_no]<tmp_mach_at_inc:
                            job_min=job_no
                            machine_min=machine_no
                            tmp_mach_at_inc=ct[job_no][machine_no]  # Current increase in machine makespan (i.e., availability time)
                            
            # Assign found task to the corresponding machine that gives the minimum completion time
            self.machin[machine_min].addTask(self.tin[job_min])
            
            # Decrement number of assigned tasks by one
            tmp_cnt-=1
            
            # Modify completion time for other tasks on found machine
            if tmp_cnt!=0:
                for i in range(len(ct)):
                    if not self.tin[i].m:
                        ct[i][machine_min]+=tmp_mach_at_inc
        
        # Record end of MINMIN running time
        self.total_computing_time = self.get_current_computing_time()
        runtime_res={'algorithm':'MINMIN','ds_id':ds_id,'iteration':iteration,'start':self.start_computing_time,'end':self.start_computing_time+self.total_computing_time,\
                'total_time':self.total_computing_time,'max_makespan':machine.getMachMaxMakespan(self.machin).makespan}
        
        # Record machines' assigned tasks, makespan and any other required properties 
        m_res=[]
        for m in self.machin:
            m_res.append({'algorithm':'MINMIN','ds_id':ds_id,'iteration':iteration,'machine_id':m.id,'tasks':\
                      [t.id for t in m.tasks],'makespan':m.makespan})
        
        # Reset machines
        machine.resetMachines(self.machin)
        
        # Return final results
        fin_res={}
        fin_res['run_time']=runtime_res
        fin_res['mach_res']=m_res
        return fin_res
        
        