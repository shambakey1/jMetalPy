'''
Created on Jan 19, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

from jmetal.problem.multiobjective.constrained import Schedule 
from jmetal.algorithm.multiobjective import bmflis
from jmetal.util.sched_utils import load_ds
from jmetal.util import machine, task

def main()->None:
    ds_prop=load_ds('/g/db/conf.json')
    objs=[{'name':'makespan','weight':1.0}]
    machin=machine.genMachines(8100, ds_prop['machines'])
    tin=task.genTasks(8100, ds_prop['tasks'])
    problem=Schedule(objs,machin,tin)
    #alg=bmflis(problem=problem)
    
if __name__ == '__main__':
    main()