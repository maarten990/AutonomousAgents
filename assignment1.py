#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from environment import *
from policy_evaluation import policy_evaluation
import sys, random

default_state = ((0, 0), (5, 5))

class random_policy:
    directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    probabilities = [0.2, 0.2, 0.2, 0.2, 0.2]
    
    def __call__(self, state):
        return add_positions(state[0], random.choice(self.directions))

def question_a(num_trials, verbose):
    simulations = [run_simulation(default_state, random_policy(), verbose) for _ in range(num_trials)]
    average = sum(simulations) / float(len(simulations))
    std_dev = sum([(simulation-average)**2 for simulation in simulations]) / float(len(simulations))

    print 'Average number of steps over {0} trials: {1:.2f}±{2:.2f}'.format(num_trials,
                                                                average,std_dev)
    
def question_b():
    state1 = ((0, 0), (5, 5))
    state2 = ((2, 3), (5, 4))
    state3 = ((2, 10), (10, 0))
    state4 = ((10, 10), (0, 0))
    V = policy_evaluation(random_policy(), gamma=0.8, verbose=verbose)

    print '{0}: {1}'.format(state1, V[state1])
    print '{0}: {1}'.format(state2, V[state2])
    print '{0}: {1}'.format(state3, V[state3])
    print '{0}: {1}'.format(state4, V[state4])

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        verbose = True
    else:
        verbose = False

    #question_a(100, verbose)
    question_b()
