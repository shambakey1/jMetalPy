'''
Created on Jan 3, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

import pandas as pd
from typing import List

from jmetal.util import machine, task
from jmetal.util.machine import Machine
from jmetal.util.task import Task
from builtins import int


def load_ds(f_path:str)->dict:
    '''
    Load dataset properties file. The input f_path is JSON file
    @param f_path: Path to input JSON file pointing to scheduling experiments configuration files
    @type f_path: String
    @return: Scehduling experimental configurations
    @rtype: dict  
    '''
    
    ds_prop_f=pd.read_json(f_path)
    ds_conf=pd.read_csv(ds_prop_f.ds_conf.path,ds_prop_f.ds_conf.sep)
    ds_cons=pd.read_csv(ds_prop_f.ds_cons.path,ds_prop_f.ds_cons.sep)
    machines=pd.read_csv(ds_prop_f.machines.path,ds_prop_f.machines.sep)
    tasks=pd.read_csv(ds_prop_f.tasks.path,ds_prop_f.tasks.sep)
    ds_prop={'conf':ds_conf,'cons':ds_cons,'machines':machines,'tasks':tasks}
    return ds_prop

def bmta(mach: List[Machine], tasks: List[Task])-> List[Task]:
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
    @return: Set of remaining unassigned tasks if any
    @rtype: List[Task]    
    '''
    machine.sortMachinesSpeed(mach)   # Sort list of machines in descending order of speed
    task.sortTaskLength(tasks)        # Sort list of tasks in descending order of length
    init_ms=sum(t.length for t in tasks)/sum(m.speed for m in mach)   # Initial equal makespan for all machines
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
    is assigned to it)
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