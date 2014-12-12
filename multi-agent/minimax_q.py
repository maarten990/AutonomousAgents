from collections import defaultdict
from environment import *
import random as rnd
from numpy import min, max, argmax
from independent_qlearning import *
from pulp import * 

def minimax_q(initial_state, gamma=0.5, explore=0.1,num_episodes=50,verbose=False):
	if len(initial_state) > 1:
		print 'Error: minimax_q only works for a single predator'
		return

	# vector of the number of steps it takes to catch the prey, used for
	# plotting. And one to decide who won
	steps = []

	# initialise variables
	pred_actions = possible_actions
	prey_actions = possible_actions

	Q  = defaultdict(lambda: 1.0)
	V  = defaultdict(lambda: 1.0)
	pi_pred = defaultdict(lambda: 1.0 / len(pred_actions))
	pi_prey = defaultdict(lambda: 1.0 / len(prey_actions))

	for episode in xrange(num_episodes):

		if verbose: print "Episode {0}".format(episode)

		state = initial_state
		num_steps = 0

		while not terminal(state):
			num_steps += 1

			alpha = 0.5

			# choose an action
			if rnd.random() < explore:
				a = rnd.choice(pred_actions)
			else:
				a = sample(pred_actions, [pi_pred[(state, action)] for action in
					pred_actions])

			if rnd.random() < explore:
				o = rnd.choice(prey_actions)
			else:
				o = sample(prey_actions, [pi_prey[(state, action)] for action in
					prey_actions])

			# learn
			pred_reward, _ = reward(state)
			newstate = step(state, [a], o)

			Q[(state, a, o)] = (1 - alpha) * Q[(state, a, o)] + alpha * (pred_reward + gamma
					* V[newstate])

			######################################## LINEAR PROGRAMMING  #############################################

			V_new  = LpVariable("V")
			p1 = LpVariable("p1", 0, 1)
			p2 = LpVariable("p2", 0, 1)
			p3 = LpVariable("p3", 0, 1)
			p4 = LpVariable("p4", 0, 1)
			p5 = LpVariable("p5", 0, 1)
			a1, a2, a3, a4, a5 = pred_actions

			prob = LpProblem("minimaxQ", LpMaximize)

			#constraints
			prob += p1 + p2 + p3 + p4 + p5 == 1 

			for o in prey_actions:
				prob += Q[(state,a1,o)]*p1 + Q[(state,a2,o)]*p2 + Q[(state,a3,o)]*p3 + Q[(state,a4,o)]*p4 + Q[(state,a5,o)]*p5 - V_new >= 0		

			# Export results
			status = prob.solve(GLPK(msg = 0))
			
			V[state] = value(V_new)
			pi_pred[(state, a1)] = value(p1)
			pi_pred[(state, a2)] = value(p2)
			pi_pred[(state, a3)] = value(p3)
			pi_pred[(state, a4)] = value(p4)
			pi_pred[(state, a5)] = value(p5)

			# update state
			state = newstate

		steps.append(num_steps)

		if verbose: print [ pi_pred[(state,a)] for a in pred_actions]	

	return steps

