'''
Created on Jul 23, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

from jmetal.problem.multiobjective.constrained import Schedule
from jmetal.core.algorithm import Algorithm
from jmetal.util import machine

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
        
        # Calculate the initial completion time matrix of all tasks over all machines
        ct=[[j.makespan+i.length/j.speed for j in self.machin] for i in self.tin]
        
        # Temporary counter to hold number of tasks that has been assigned to machines
        tmp_cnt=len(ct)
        
        # Repeat until all tasks are assigned
        while tmp_cnt!=0:
            machine_min=-1      # Machine index with minimum completion time (initialized to -1 which corresponds to no machine)
            job_min_ls=[]       # List with tasks and the 
            tmp_max_ct=sys.float_info.max   # Maximum completion time (initialized to maximum float value)
            tmp_min_ct=0.0                  # Minimum completion time (initialized to 0.0)
            
            # Traverse all completion time job by job to find the machine for each job with minimum completion time
            for job_no in range(len(ct)):
                if not self.tin[job_no].m:
                    for machine_no in range(len(ct[0])):
                        if ct[job_no][machine_no]<=tmp_max_ct:
                            machine_min=machine_no
                            tmp_max_ct=ct[job_no][machine_no]  # Current increase in machine makespan (i.e., availability time)
                    # Add current job with machine that gives minimum completion time to the list job_min_ls
                    job_min_ls.append([job_no,machine_min])
                    # Reset tmp_max_ct to be used in the comparison of the next job, as well as machine_min
                    tmp_max_ct=sys.float_info.max
                    machine_min=-1
                            
            # Find the task in job_min_ls with maximum completion time
            for i in job_min_ls:
                if ct[i[0]][i[1]]>=tmp_min_ct:
                    job_max_min=i[0]
                    machine_max_min=i[1]
                    tmp_min_ct=ct[i[0]][i[1]]
                    
            # Assign found task to the corresponding machine that gives the max-min completion time
            self.machin[machine_max_min].addTask(self.tin[job_max_min])
            
            # Decrement number of assigned tasks by one
            tmp_cnt-=1
            
            # Modify completion time for other tasks on found machine
            if tmp_cnt!=0:
                for i in range(len(ct)):
                    if not self.tin[i].m:
                        ct[i][machine_max_min]+=tmp_min_ct
        
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
        
        