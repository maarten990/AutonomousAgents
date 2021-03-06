from environment import *
from independent_qlearning import *
from random import choice
import numpy as np
import os.path
import time

def batch_run(batch_settings,n=50,num_episodes=10000):

	for i,current_batch in enumerate(batch_settings):

		# Import settings
		algorithm    = current_batch[0]
		algo_func    = current_batch[1]
		changevar	 = current_batch[2]
		var_value	 = current_batch[3]
		num_pred     = current_batch[4]


		filebase = "data/{0}.p={1},{2}={3}".format(algorithm,num_pred,changevar,var_value)
		if os.path.isfile(filebase+ '.winners.csv') and  os.path.isfile(filebase+ '.steps.csv'):
			print 'Experiment allready contucted, skiping . . .'
		else:
			print 'Running batch {0}/{1}'.format(i,len(batch_settings))

			#create dummy files, so this calculations will be skipped by parralel scripts
			#open(filebase+ '.winners.csv', 'w').close()
			#open(filebase+ '.steps.csv', 'w').close()

			# Make state
			if num_pred == 1:
				state = initialise_state([(10, 10)], (5, 5))
			elif num_pred ==2:
				state = initialise_state([(10, 10), (10, 0)], (5, 5))
			elif num_pred ==3:
				state = initialise_state([(10, 10), (10, 0), (0, 10)], (5, 5))	
			elif num_pred ==4:
				state = initialise_state([(10, 10), (10, 0), (0, 10),(0, 0)], (5, 5))	
			else:
				print 'ERROOROROREOROEROEROERORREORO'

			# Preallocate
			winners_mat = [];
			steps_mat = [];

			t0 = time.time()

			# Run all the trials 
			for _ in range(n):

				# DO IT BABY
				s, w = eval(algo_func + "(state, num_episodes={0}, {1}={2})".format(num_episodes,changevar,var_value))

				winners_mat.append(w)
				steps_mat.append(s)


			duurtlang = time.time() - t0
			if duurtlang < 60:
				print "{0:.2f}sec elapsed".format(duurtlang)
			elif duurtlang < 60*60:
				print "{0:.2f}min elapsed".format(duurtlang/60)
			elif duurtlang < 60*60*24:
				print "{0:.2f}h elapsed".format(duurtlang/60/60)
			else:
				print "fucking lang elapsed"

			#Store results
			np.savetxt(filebase + '.winners.csv',winners_mat)
			np.savetxt(filebase + '.steps.csv',steps_mat)


#General settings
num_preds    = [1, 2, 3, 4]
num_trials   = 25
num_episodes = 10000
algorithm    = "Q"
algo_func    = "independent_qlearning"


#Lang code whaaat: 
###########################################################################################
batch_settings = [('Q',"independent_qlearning",'gamma',g,2) for g in [0.7, 0.9]]
for n, line in enumerate(batch_settings):
	print n, line
batch_run(batch_settings,num_trials,num_episodes)
#############################################################################


#Speficif experiments
alphas	    = [0.1, 0.2, 0.3, 0.4, 0.5]
gammas      = [0.1, 0.5, 0.7, 0.9]
epsilons    = [0,0.1,0.5,0.9]
init_values = [0, 5, 15, 50]
taus	    = [0.1, 0.5,1,5]


#batch_settings = [(algorithm, algo_func, changevar, var_value, 1), (algorithm, algo_func, changevar, var_value, 2)]
batch_settings = []
batch_settings = batch_settings + [(algorithm, algo_func, 'alpha', 		   a, p) for p in num_preds for a in alphas ]
batch_settings = batch_settings + [(algorithm, algo_func, 'gamma', 		   g, p) for p in num_preds for g in gammas ]
batch_settings = batch_settings + [(algorithm, algo_func, 'initial_value', v, p) for p in num_preds for v in init_values ]

batch_settings = batch_settings + [(algorithm, algo_func, 'selection_func', 'epsilon_greedy({0})'.format(e), p) for p in num_preds for e in epsilons ]
#batch_settings = batch_settings + [(algorithm, algo_func, 'selection_func', 'softmax({0})'.format(t),	     p) for p in num_preds for t in taus ]


#For edwin, the other way around
#batch_settings.reverse()

for n, line in enumerate(batch_settings):
	print n, line

batch_run(batch_settings,num_trials,num_episodes)