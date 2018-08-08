'''
Created on Jan 3, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

import pandas as pd
import yaml
from typing import List

from jmetal.util import machine, task
from jmetal.util.machine import Machine, getMachMaxMakespan
from jmetal.util.task import Task
from builtins import int

import sys
from asyncio import tasks


def load_ds(f_path:str)->dict:
    '''
    Load dataset properties file. The input f_path is JSON file
    @param f_path: Path to input JSON file pointing to scheduling experiments configuration files
    @type f_path: String
    @return: Scehduling experimental configurations
    @rtype: dict  
    '''
    
    #ds_prop_f=pd.read_json(f_path)
    with open(f_path,'r') as f:
    	ds_prop_f=yaml.load(f)
    
    ds_conf=pd.read_csv(ds_prop_f['ds_conf']['path'],ds_prop_f['ds_conf']['sep'])
    ds_cons=pd.read_csv(ds_prop_f['ds_cons']['path'],ds_prop_f['ds_cons']['sep'])
    machines=pd.read_csv(ds_prop_f['machines']['path'],ds_prop_f['machines']['sep'])
    tasks=pd.read_csv(ds_prop_f['tasks']['path'],ds_prop_f['tasks']['sep'])
    objs=ds_prop_f['objectives']
    algs=ds_prop_f['algorithms']
    res_path=ds_prop_f['results_path']
    ds_ids=ds_prop_f['ds_id']
    iterations=ds_prop_f['iter']
    ds_prop={'conf':ds_conf,'cons':ds_cons,'machines':machines,'tasks':tasks,'objectives':objs,\
             'algorithms':algs,'results_path':res_path,'ds_ids':ds_ids,'iterations':iterations}
    return ds_prop

def th_makespan(mach: List[Machine], tasks: List[Task])->float:
    ''' Calculate theoretical bound on makespan for uniform parallel machines as given by Lemma 5.2.10 in the 
    book of 'Scheduling Theory, Algorithms, and Systems' fourth edition. The theoritical makespan bound is cal-
    culated by the sum of lengths of the longest k tasks over the sum of the speeds of the k fastest machines.
    @param mach: List of machines to assign tasks
    @type mach: List[Machines]
    @param tasks: List of task to assign to machines
    @type tasks: List[Task]
    @return: Theoretical makespan
    @rtype: float
    '''
    machine.sortMachinesSpeed(mach)   # Sort list of machines in descending order of speed
    task.sortTaskLength(tasks)        # Sort list of tasks in descending order of length
    
    n=len(tasks)    # Number of tasks
    m=len(mach)     # Number of machines
    k=max(n,m)      # Holds maximum between number of tasks and number of machines
    len_sum=0       # Holds current sum of jobs lengths
    speed_sum=0     # Holds current sum of machines speeds
    th_makespan=0   # Holds theoretical makespan
    
    for i in range(k):
        if tasks[i]:
            len_sum+=tasks[i].length
        if mach[i]:
            speed_sum+=mach[i].speed
        if th_makespan<len_sum/speed_sum:
            th_makespan=len_sum/speed_sum
        return th_makespan
     
   
def bmta(mach: List[Machine], tasks: List[Task], th_per:float=0.0)-> List[Task]:
    ''' Balanced Makespan Task Assignment algorithm: one way to assign tasks to machines with \
    approximately equal (as much as possible) makespan for each machine. Currently, the order of tasks in \
    the same machine is not important. The algorithm works by assuming initial equal makespan for all machines. \
    The initial phase investigates machines in non-increasing order of speed, and tasks in non-increasing \
    order of length. Tasks are added to each machine as long as the initial makespan allows. Second phase \
    assigns tasks to machines on least-makespan increase basis
    @param mach: List of machines to assign tasks
    @type mach: List[Machines]
    @param tasks: List of task to assign to machines
    @type tasks: List[Task]
    @param th_per: Threshold percentage that should be added over the theoritical bound on makespan to allow for more tasks to be assigned to each machine
    @type th_per: float  
    @return: Set of remaining unassigned tasks if any
    @rtype: List[Task]    
    '''
    machine.sortMachinesSpeed(mach)   # Sort list of machines in descending order of speed
    task.sortTaskLength(tasks)        # Sort list of tasks in descending order of length
    #tmp_max_makespan=sum(t.length for t in tasks)/mach[0].speed         # Initial max makespan calculated as the sum of lengths of all tasks when executed on the fastest machine
    #init_ms=sum(t.length for t in tasks)/sum(m.speed for m in mach)   # Initial equal makespan for all machines
    init_ms=th_makespan(mach, tasks)   # Initial equal makespan for all machines
    #init_ms+=(tmp_max_makespan-init_ms)*th_per
    for m in mach:  # Check machine in descending order of speed
        init_ms_cp=init_ms  # Set initial makespan for current machine
        tmp_tasks=[]    # Holds remaining tasks for next machine
        for t in tasks:  # Check tasks in descending order of length
            if t.length<=m.speed*init_ms_cp and init_ms_cp:    # Check if next task can be added to current machine
                m.addTask(t)    # Add new task to current machine (modify makespan of current machine, and 
                                # assign current machine to the task)
                init_ms_cp-=t.length/m.speed    # Modify the initial equal makespan for each machine as the task is assigned to current machine
            else:
                tmp_tasks.append(t) # Add task to remaining set of tasks
        tasks=tmp_tasks # Update investigated tasks to remaining set of tasks
    return tasks

def lmita(mach: List[Machine],tasks:List[Task])->None:
    ''' Allocate independent set of tasks on heterogeneous machines according to least-makespan increase basis \
    (i.e., current task is allocated to the machine that will have the least increase in makespan when this task \
    is assigned to it). Tasks are investigated non-increasing order of lengths. Machines are investigated in 
    non-increasing order of speed.
    @param mach: List of machines
    @type mach: List[Machine]
    @param tasks: List of tasks
    @type tasks: List[Task]
    '''
	
    machine.sortMachinesSpeed(mach)   # Sort list of machines in descending order of speed
    task.sortTaskLength(tasks)        # Sort list of tasks in descending order of length
    for t in tasks:
        tmp_ms=float('inf')  # Temporary makespan holding makespan if t is added to machine m
        tmp_m=None  # Temporary machine variable
        for m in mach:
            if m.makespan+t.length/m.speed<tmp_ms:  # Check if adding current task to current machine produces smaller total makespan
                tmp_m=m # Current machine is a candidate to run current task
                tmp_ms=m.makespan+t.length/m.speed  # Modify temporary makespan
        tmp_m.addTask(t)    # Assign current task to the machine with least makespan increase

def redTasks(mach: List[Machine],tasks:List[Task])->None:
    ''' Redistributed tasks from the machine with maximum makespan, using @lmita algorithm, if this will reduce makespan
    @param mach: List of machines
    @type mach: List[Machine]
    @param tasks: List of tasks
    @type tasks: List[Task]
    '''
    
    # Find the machine with maximum completion time (i.e., maximum makespan)
    m=getMachMaxMakespan(mach)
    
    # Find current makespan before re-assigning tasks
    makespan_before=m.makespan
    
    # Retrive list of tasks from the machine with maximum makespan arranged in ascending order of length
    m_ts=m.tasks.copy()
    task.sortTaskLength(m_ts,False) 
    
    # Loop until maximum makespan cannot be reduced any more, or all tasks from machine, with maximum makespan, are re-assigned
    while m_ts:
        
        # Find the shortest task on the machine
        st=m_ts[0]
        
        # Remove shortest task from the machine with maximum makespan
        m.remTask(st)
        
        # Add shortest task to the machine that causes minimum increase in completion 
        lmita(mach,[st])
        
        # Extract the new makespan
        m_after=getMachMaxMakespan(mach)
        makespan_after=m_after.makespan
        
        # If the new makespan is not improved, then restore last task distribution, then exit.
        #Otherwise, continue distributing tasks
        if makespan_before<makespan_after:
            m_ass=st.m  # The machine to which the shortest task is re-assigned
            m_ass.remTask(st)
            m.addTask(st)
            break
        else:
            m_ts.remove(st)
            makespan_before=makespan_after
        

def maxmin_core(mach: List[Machine],tasks:List[Task],ct=None)->None:
    ''' The core code of the Max-Min scheduling algorithm. The algorithm starts by determining for each task 
    the machine with corresponding minimum completion time. Each task with the corresponding machine of minimum 
    completion time is added to a list. Then, among the tasks in the list, the task with the maximum completion 
    time is selected first to be mapped to the corresponding machine. This process is repeated until all tasks 
    are allocated.
    @param mach: List of machines
    @type mach: List[Machine]
    @param tasks: List of tasks
    @type tasks: List[Task]
    '''
    
    # Calculate the initial completion time matrix of all tasks over all machines
    if not ct:
        ct=[]
        for i in range(len(tasks)):
            ct.append([])
            if (not tasks[i].m) or (tasks[i].m==-1): # Make sure that task i has not already been allocated
                for j in range(len(mach)):
                    ct[i].append(mach[j].makespan+tasks[i].length/mach[j].speed)
    
    # Temporary counter to hold number of tasks that has been assigned to machines
    tmp_cnt=len(tasks)
    
    # Repeat until all tasks are assigned
    while tmp_cnt!=0:
        machine_min=-1      # Machine index with minimum completion time (initialized to -1 which corresponds to no machine)
        job_min_ls=[]       # List with tasks and the 
        tmp_max_ct=sys.float_info.max   # Maximum completion time (initialized to maximum float value)
        tmp_min_ct=0.0                  # Minimum completion time (initialized to 0.0)
        
        # Traverse all completion time job by job to find the machine for each job with minimum completion time
        for job_no in range(len(tasks)):
            if (not tasks[job_no].m) or (tasks[job_no].m==-1):
                for machine_no in range(len(mach)):
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
        if job_min_ls:  # Check job_min_ls is not empty
            mach[machine_max_min].addTask(tasks[job_max_min])
        
        # Decrement number of assigned tasks by one
        tmp_cnt-=1
        
        # Modify completion time for other tasks on found machine
        if tmp_cnt>=0:
            for i in range(len(tasks)):
                if (not tasks[i].m) or (tasks[job_no].m==-1):
                    ct[i][machine_max_min]+=tmp_min_ct
        
def maxmin_makespan_thr_core(mach: List[Machine],tasks:List[Task],makespan_in)->None:
    ''' This function acts as @maxmin_core function except that the tasks are allocated to machines as the initial 
    makespan of each machine does not exceed a given threshold in the first phase. In the second phase, the 
    remaining tasks from the first phase are allocated normally as maxmin
    @param mach: List of machines
    @type mach: List[Machine]
    @param tasks: List of tasks
    @type tasks: List[Task]
    @param makespan_thr: Makespan threshold for first phase of assignment
    @type makespan_thr: Double
    '''
    
    # Keep a copy of the makespan input threshold
    makespan_thr=makespan_in
    
    # Calculate the initial completion time matrix of all tasks over all machines
    ct=[]
    for i in range(len(tasks)):
        ct.append([])
        if (not tasks[i].m) or (tasks[i].m==-1): # Make sure that task i has not already been allocated
            for j in range(len(mach)):
                ct[i].append(mach[j].makespan+tasks[i].length/mach[j].speed)
        
    # Temporary counter to hold number of tasks that has been assigned to machines
    tmp_cnt=len(ct)
    
    # Tasks are allocated in MAXMIN way as long as completion time does not exceed makespan threshold.
    # Remaining tasks (i.e., tasks whose allocated machines are -1) are allocated some other way (e.g., original MAXMIN without makespan threshold)
    while tmp_cnt!=0:
        machine_min=-1      # Machine index with minimum completion time (initialized to -1 which corresponds to no machine)
        job_min_ls=[]       # List with tasks and the 
        tmp_max_ct=makespan_thr   # Maximum completion time (initialized to makespan threshold)
        tmp_min_ct=0.0      # Minimum completion time (initialized to 0.0)
        machine_max_min=-1  # Machine with maximum completion time for job among list of jobs with minimum completion times 
        job_max_min=-1      # Task with maximum completion time among list of jobs with minimum completion times
        
        # Traverse all completion time job by job to find the machine for each job with minimum completion time
        for job_no in range(len(tasks)):
            if (not tasks[job_no].m):    # Make sure the job hasn't been already allocated, nor already been investigated (i.e., machine=-1)
                for machine_no in range(len(mach)):
                    if ct[job_no][machine_no]<=tmp_max_ct:
                        machine_min=machine_no
                        tmp_max_ct=ct[job_no][machine_no]  # Current increase in machine makespan (i.e., availability time)
                # Add current job with machine that gives minimum completion time to the list job_min_ls
                job_min_ls.append([job_no,machine_min])
                if machine_min==-1:
                    tasks[job_no].m=-1
            # Reset tmp_max_ct to be used in the comparison of the next job, as well as machine_min
            tmp_max_ct=makespan_thr
            machine_min=-1
                        
        # Find the task in job_min_ls with maximum completion time that does not exceed the makespan threshold (i.e., machine_min!=-1) 
        for i in job_min_ls:
            if ct[i[0]][i[1]]>=tmp_min_ct and i[1]!=-1:
                job_max_min=i[0]
                machine_max_min=i[1]
                tmp_min_ct=ct[i[0]][i[1]]
                
        # Assign found task, if any, to the corresponding machine that gives the max-min completion time
        if job_max_min!=-1:
            mach[machine_max_min].addTask(tasks[job_max_min])
        else:   # No task with completion time that is less than makespan threshold. So, go to the second phase
            break
        
        # Decrement number of assigned tasks by one
        tmp_cnt-=1
        
        # Modify completion time for other tasks on found machine
        if tmp_cnt>=0 and job_max_min!=-1:
            for i in range(len(ct)):
                if not tasks[i].m:
                    ct[i][machine_max_min]+=tmp_min_ct
                
        # Return ct to be used by another scheduling algorithm
        return ct
    
    # Phase 2: Assign tasks in the normal MAXMIN algorithm