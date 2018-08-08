'''
Created on Jul 22, 2018

@author: shambakey1
@contact: shambakey1@gmail.com
'''

from jmetal.problem.multiobjective.constrained import Schedule 
from jmetal.algorithm.multiobjective.bmflis import BMFLIS
from jmetal.algorithm.multiobjective.minmin import MINMIN
from jmetal.algorithm.multiobjective.maxmin import MAXMIN
from jmetal.algorithm.multiobjective.bmfmms import BMFMMS
from jmetal.algorithm.multiobjective.m3fm2s import M3FM2S
from jmetal.util.sched_utils import load_ds
from jmetal.util import machine, task
import os, time
import pandas as pd

def main()->None:
    # Load experiments configuration file
    ds_prop=load_ds('/g/db/scheduling_dataset/conf.yml')
    
    # Specify objectives
    objs=ds_prop['objectives']
    
    # Path to final results
    res_idx=str(time.time())
    res_running_time=os.path.join(ds_prop['results_path'],(res_idx+'_running_time.csv'))
    res_machines=os.path.join(ds_prop['results_path'],(res_idx+'_machines.csv'))
    
    # Number of iterations for each experiment
    iterations=ds_prop['iterations']
    
    # Final results (including running time of each algorithm and updated machines' status)
    final_res={'run_time':[],'mach_res':[]}
    
    # Specify required datasets for analysis
    if 'all' in ds_prop['ds_ids']:
        ds_prop_ids=ds_prop['conf']['id']
    else:
        ds_prop_ids=ds_prop['ds_ids']
    
    # Traverse through different experiments
    for ds_id in ds_prop_ids:
        machin=machine.genMachines(ds_id, ds_prop['machines'])
        tin=task.genTasks(ds_id, ds_prop['tasks'])
        problem=Schedule(objs,machin,tin)
        
        # Traverse through different algorithms for experiments
        for alg_id in ds_prop['algorithms']:
            
            # BMFLIS algorithm
            if alg_id=='BMFLIS':
                alg=BMFLIS(problem=problem)
                for i in range(iterations):
                    res=alg.run(ds_id=ds_id,iteration=i,th_per=0.0)
                    final_res['run_time'].append(res['run_time'])
                    final_res['mach_res'].extend(res['mach_res'])
                    print('Algorithm:BMFLIS, dataset: '+str(ds_id)+', iteration: '+str(i))
            # MINMIN algorithm
            elif alg_id=='MINMIN':
                alg=MINMIN(problem=problem)
                for i in range(iterations):
                    res=alg.run(ds_id=ds_id,iteration=i)
                    final_res['run_time'].append(res['run_time'])
                    final_res['mach_res'].extend(res['mach_res'])
                    print('Algorithm:MINMIN, dataset: '+str(ds_id)+', iteration: '+str(i))
            # MAXMIN algorithm
            elif alg_id=='MAXMIN':
                alg=MAXMIN(problem=problem)
                for i in range(iterations):
                    res=alg.run(ds_id=ds_id,iteration=i)
                    final_res['run_time'].append(res['run_time'])
                    final_res['mach_res'].extend(res['mach_res'])
                    print('Algorithm:MAXMIN, dataset: '+str(ds_id)+', iteration: '+str(i))
            # BMFMMS algorithm
            elif alg_id=='BMFMMS':
                alg=BMFMMS(problem=problem)
                for i in range(iterations):
                    res=alg.run(ds_id=ds_id,iteration=i)
                    final_res['run_time'].append(res['run_time'])
                    final_res['mach_res'].extend(res['mach_res'])
                    print('Algorithm:BMFMMS, dataset: '+str(ds_id)+', iteration: '+str(i))
            # M3FM2S algorithm
            elif alg_id=='M3FM2S':
                alg=M3FM2S(problem=problem)
                for i in range(iterations):
                    res=alg.run(ds_id=ds_id,iteration=i)
                    final_res['run_time'].append(res['run_time'])
                    final_res['mach_res'].extend(res['mach_res'])
                    print('Algorithm:BMFMMS, dataset: '+str(ds_id)+', iteration: '+str(i))
                    
    # Record running time results
    with open(res_running_time,'a') as f:
        d=pd.DataFrame(final_res['run_time'])
        d.to_csv(f,index=False)
        
    # Record machines results (e.g., assigned tasks, makespan for each machine)
    with open(res_machines,'a') as f:
        d=pd.DataFrame(final_res['mach_res'])
        d.to_csv(f,index=False)
    
if __name__ == '__main__':
    main()