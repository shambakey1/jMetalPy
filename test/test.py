'''
Created on Mar 18, 2018

@author: Mohammed Elshambakey
@contact: shambakey1@gmail.com
'''
import sys,jmetal
from jmetal.problem.multiobjective.constrained import Schedule
from jmetal.util.sched_utils import load_ds
from builtins import str
from jmetal.util.machine import genMachines, getMachMaxMakespan
from jmetal.util.task import genTasks
from jmetal.problem.multiobjective.constrained import Schedule
from jmetal.algorithm.multiobjective.bmflis import BMFLIS

	
def testBMTLIS(exp_conf_path:str):
	''' Test BMFLIS which includes LMITA and BMTA 
	@param exp_conf_path: Configuration file path (in YAML)
	@type exp_conf_path: str  
	'''
	ds_id=8100
	
	if not exp_conf_path:
		print('Error: configuration path cannot be empty')
	else:
		conf=load_ds(exp_conf_path)	# Load configuration file for datasets
		if 'all' in conf['ds_id']:
			#TODO: use all datasets for experiments
		else:
			ds_ids=conf['ds_id']	# Use only specified datasets for experiments
			'''
		objs=conf['objectives']
		machines=conf['machines']
		tasks=conf['tasks']
		machin=genMachines(ds_id,machines)
		tin=genTasks(ds_id,tasks)
		problem=Schedule(objs,machin,tin)
		alg=BMFLIS(problem)
		alg.run()
		print()
		for m in machin:
			print('Machine ID: '+str(m.id)+', speed: '+str(m.speed)+', makespan: '+str(m.makespan)+', tasks: '+str([x.id for x in m.tasks]))
		print()
		max_mach=getMachMaxMakespan(machin)
		print('Maximum makespan machine: '+str(max_mach.id)+', makespan: '+str(max_mach.makespan)+', tasks: '+str([t.id for t in max_mach.tasks]))
	'''

if __name__ == '__main__':
	testBMTLIS('conf.yml')
	