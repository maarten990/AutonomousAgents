#!/usr/bin/env python2
# coding=utf-8

from environment import *
from policy_evaluation import policy_evaluation
from policy_improvement import policy_improvement
from value_iteration import value_iteration
import random, argparse

default_state = (5, 5)

class random_policy:
    "Random policy that mimicks a dictionary"
    directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    probabilities = [0.2, 0.2, 0.2, 0.2, 0.2]
    
    def __getitem__(self, state):
        return random.choice(self.directions)

def print_policy(policy, prey_position):
    """
    Print the optimal move given a policy for each predator given a fixed
    position for the prey.
    """
    grid = [['_' for _ in range(11)] for _ in range(11)]
    prey_x, prey_y = prey_position
    arrowmap = {
        (-1, 0): u'←',
        (0, -1): u'↑',
        (1, 0): u'→',
        (0, 1): u'↓',
        (0, 0): u' ',
    }

    # translate from positions to the distance representation
    for x in range(11):
        for y in range(11):
            state = (x - prey_x, y - prey_y)
            grid[y][x] = arrowmap[policy[state]]

    grid[prey_x][prey_y] = u'☃'

    print ' _ _ _ _ _ _ _ _ _ _ _'
    for row in grid:
        print '|' + '|'.join(row) + '|'
    print '\n'
    

# run a bunch of simulations on the default state using a random policy
def question_a(verbose, num_trials=100):
    simulations = [run_simulation(default_state, random_policy(), verbose) for _ in range(num_trials)]
    average = sum(simulations) / float(len(simulations))
    std_dev = sum([(simulation-average)**2 for simulation in simulations]) / float(len(simulations))

    if verbose:
        print 'Counts: '
        print '\n'.join(map(str, simulations))

    print 'Average number of steps over {0} trials: {1:.2f}±{2:.2f}'.format(num_trials,
                                                                average,std_dev)
    
# perform policy evaluation and print the V values of several states
def question_b(verbose):
    state1 = (-5, -5)
    state2 = (-3, -1)
    state3 = (3, -1)
    state4 = (1, 1)

    V = policy_evaluation(random_policy(), gamma=0.8, verbose=verbose)

    print '{0}: {1}'.format(state1, V[state1])
    print '{0}: {1}'.format(state2, V[state2])
    print '{0}: {1}'.format(state3, V[state3])
    print '{0}: {1}'.format(state4, V[state4])

# perform policy iteration and print the policy for all states where the prey is at (5, 5)
def question_c(verbose):
    # create the policy and and print it for a prey at (5, 5)
    policy = policy_improvement(gamma=0.8, verbose=verbose)
    print_policy(policy, (5, 5))
    
    # run the simulation a few times just for shits and giggles
    simulations = [run_simulation(default_state, policy, verbose) for _ in range(100)]
    average = sum(simulations) / float(len(simulations))
    std_dev = sum([(simulation-average)**2 for simulation in simulations]) / float(len(simulations))

    print 'Average number of steps over {0} trials: {1:.2f}±{2:.2f}'.format(100, average, std_dev)

# perform value iteration and print the policy for all states where the prey is at (5, 5)
def question_d(verbose):
    # create the policy and and print it for a prey at (5, 5)
    policy = value_iteration(gamma=0.8, verbose=verbose)
    print_policy(policy, (5, 5))

    # run the simulation a few times just for shits and giggles
    simulations = [run_simulation(default_state, policy, verbose) for _ in range(100)]
    average = sum(simulations) / float(len(simulations))
    std_dev = sum([(simulation-average)**2 for simulation in simulations]) / float(len(simulations))

    print 'Average number of steps over {0} trials: {1:.2f}±{2:.2f}'.format(100, average, std_dev)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('question', help='the subquestion to execute',
            choices=['a', 'b', 'c', 'd'])
    parser.add_argument('-v', '--verbose', help='produce more verbose output',
            action='store_true')

    args = parser.parse_args()
    eval('question_{0}'.format(args.question))(args.verbose)
