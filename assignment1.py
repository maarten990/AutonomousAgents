#!/usr/bin/env python2
# coding=utf-8

from environment import *
from policy_evaluation import policy_evaluation
from policy_improvement import policy_improvement
import sys, random

default_state = ((0, 0), (5, 5))

class random_policy:
    "Random policy that mimicks a dictionary"
    directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    probabilities = [0.2, 0.2, 0.2, 0.2, 0.2]
    
    def __getitem__(self, state):
        return random.choice(self.directions)

# run a bunch of simulations on the default state using a random policy
def question_a(num_trials, verbose):
    simulations = [run_simulation(default_state, random_policy(), verbose) for _ in range(num_trials)]
    average = sum(simulations) / float(len(simulations))
    std_dev = sum([(simulation-average)**2 for simulation in simulations]) / float(len(simulations))

    print 'Average number of steps over {0} trials: {1:.2f}±{2:.2f}'.format(num_trials,
                                                                average,std_dev)
    
# perform policy evaluation and print the V values of several states
def question_b(verbose):
    state1 = ((0, 0), (5, 5))
    state2 = ((2, 3), (5, 4))
    state3 = ((2, 10), (10, 0))
    state4 = ((10, 10), (0, 0))

    V = policy_evaluation(random_policy(), gamma=0.8, verbose=verbose)

    print '{0}: {1}'.format(state1, V[state1])
    print '{0}: {1}'.format(state2, V[state2])
    print '{0}: {1}'.format(state3, V[state3])
    print '{0}: {1}'.format(state4, V[state4])

# perform policy iteration and print the policy for all states where the prey is at (5, 5)
def question_c(verbose):
    # visualize directions
    arrowmap = {
        (-1, 0): u'←',
        (0, -1): u'↑',
        (1, 0): u'→',
        (0, 1): u'↓',
        (0, 0): u' ',
    }

    # create the policy and filter it to the states we're interested in
    policy = policy_improvement(gamma=0.8, verbose=verbose)
    relevant = {state: direction for state, direction in policy.iteritems()
                if state[1] == (5, 5)}

    # draw!
    grid = [['_' for _ in range(11)] for _ in range(11)]

    for state, direction in relevant.iteritems():
        predator, _ = state
        x, y = predator
        grid[y][x] = arrowmap[direction]

    grid[5][5] = u'☃'

    print ' _ _ _ _ _ _ _ _ _ _ _'
    for row in grid:
        print u'|' + u'|'.join(row) + u'|'
    print '\n'
    
    # run the simulation a few times just for shits and giggles
    simulations = [run_simulation(default_state, policy, verbose) for _ in range(100)]
    average = sum(simulations) / float(len(simulations))
    std_dev = sum([(simulation-average)**2 for simulation in simulations]) / float(len(simulations))

    print 'Average number of steps over {0} trials: {1:.2f}±{2:.2f}'.format(100, average, std_dev)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        verbose = True
    else:
        verbose = False

    #question_a(100, verbose)
    #question_b(verbose)
    question_c(verbose)
