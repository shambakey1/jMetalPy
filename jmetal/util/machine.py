'''
Created on Jan 3, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''
from builtins import int
from jmetal.util.task import Task
from typing import List
from pandas import DataFrame

class Machine(object):
    '''
    Different machine types (e.g., VM, core, processor)
    '''


    def __init__(self, ds_conf_id:int,machine_id:int,speed:float,cost:float=0.0,energy:float=0.0,tasks:List[Task]=[]):
        ''' Initialize list of machines from input machine configuration that correspond to dataset id
        @param ds_conf_id: The specific dataset ID 
        @type ds_conf_id: int
        @param machine_id: Machine ID
        @type machine_id: int
        @param speed: Machine speed 
        @type speed: float
        @param tasks: Optional set of tasks assigned to current machine instance
        @type tasks: List of job instances 
        @param cost: Cost per time unit for current machine
        @type cost: float
        @param energy: Energy consumption for current machine
        @type energy: float
        '''
        
        self.ds_conf_id=int(ds_conf_id)
        self.id=int(machine_id)
        self.speed=float(speed)
        self.makespan=0.0   # Makespan of current machine is the same as availability time of current machine
        self.cost=cost
        self.energy=energy
        self.tasks=[]
        for t in tasks:
            self.addTask(t)
    
    def addTask(self,t:Task)->None:
        ''' Add a task to current machine
        @param t: Task to be added to current machine
        @type t: Task
        '''  
        self.tasks.append(t)    # Add task to task list of current machine. Currently, addition order is not important
        self.makespan+=t.length/self.speed  # Modify makespan of current machine
        t.m=self    # Assign current machine to input task. TODO: This may lead to spaghetti programming
    
    def remTask(self,t:Task)->None:
        ''' Remove specified task from current machine
        @param t: Task to be removed to current machine
        @type t: Task
        '''
        self.tasks.remove(t)
        self.makespan-=t.length/self.speed
        t.m=None
        
    def resetMachine(self)->None:
        ''' Remove any assigned tasks to this machine, as well as remove the machine from the task 
        '''

        for t in self.tasks:
            t.m=None
        self.tasks=[]
        self.makespan=0.0
        
def sortMachinesSpeed(mach: List[Machine],desc:bool=True)->None:
    ''' Sort List of machines according to descending order of machine speed.
    @param mach: List of machines to be ordered
    @type mach: List[Machine]
    @param desc: Sorting order (default is true)
    @type desc: bool
    '''
    from operator import attrgetter
    mach.sort(key=attrgetter('speed'),reverse=desc)

def sortMachinesID(mach: List[Machine],desc:bool=False)->None:
    ''' Sort List of machines according to ascending order of machines IDs.
    @param mach: List of machines to be ordered
    @type mach: List[Machine]
    @param desc: Sorting order (default is false)
    @type desc: bool
    '''
    from operator import attrgetter
    mach.sort(key=attrgetter('id'),reverse=desc)

def genMachines(ds_id:int, mach_conf:DataFrame)-> List[Machine]:
    '''
    Generate set of machines from input machine configuration
    @param mach_conf: Input machine configuration file which contains configurations for all experiments. The important columns are 'machine_id' and 'speed'
    @type mach_conf: DataFrame
    @param ds_id: Specific dataset ID to read machine configurations
    @type ds_id: int
    @return: Machine set of current dataset ID configuration
    @rtype: List[Machine]    
    '''
    
    import copy
    
    return copy.deepcopy([Machine(ds_id,i.machine_id,i.speed) for i in mach_conf.itertuples() if i.dataset_conf_id==ds_id])
   
def getMachMaxMakespan(mach: List[Machine])->Machine:
	''' Extract the machine from the input list with maximum makespan
	@param mach: List of machines
	@type mach: List[Machine]  
	@return: Machine with maximum makespan
	@rtype: Machine
	'''
	
	max_makespan=0.0
	max_m=None
	for m in mach:
		if m.makespan>max_makespan:
			max_m=m
			max_makespan=m.makespan
	return max_m

def resetMachines(mach: List[Machine])->None:
    ''' Clean assigned tasks for set of machines
    '''
    
    for m in mach:
        m.resetMachine()
	
