'''
Created on Jan 3, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''
from pandas import DataFrame
from typing import List

class Task():
    '''
    Task class
    '''


    def __init__(self, ds_conf_id,task_id,length,m=None):
        '''
        Task constructor
        @param ds_conf_id: Dataset ID to which this task instance belongs
        @type ds_conf_id: Integer
        @param task_id: Task ID
        @type task_id: int  
        @param length: Length of this task instance
        @type length: float
        @return: Task instance
        @param m: Optional machine to run the task instance. Machine can change later. Initiallly, the task may not be assigned to any machine
        @type m: Machine  
        @rtype: Task    
        '''
        
        self.ds_conf_id=int(ds_conf_id)
        self.id=task_id
        self.length=float(length)
        self.m=m
        
def sortTaskLength(tasks: List[Task],desc:bool=True)->None:
    ''' Sort List of tasks according to descending order of task length
    @param tasks: List of tasks to be ordered
    @type tasks: List[Task]
    @param desc: Sorting order (default is true)
    @type desc: bool
    '''
    from operator import attrgetter
    tasks.sort(key=attrgetter('length'),reverse=desc)

def genTasks(ds_id:int, task_conf:DataFrame)->List[Task]:
    '''
    Generate set of tasks from input task configuration
    @param task_conf: Input task configuration file which contains configurations for all experiments. The important columns are 'task_id' and 'length'
    @type mach_conf: DataFrame
    @param ds_id: Specific dataset ID to read task configurations
    @type ds_id: int
    @return: Task set of current dataset ID configuration
    @rtype: List[Task]    
    '''
    
    return [Task(ds_id,i.task_id,i.length) for i in task_conf.itertuples() if i.dataset_conf_id==ds_id]