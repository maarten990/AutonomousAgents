#!/usr/bin/env python2
# coding=utf-8

from environment import *
from qlearning import *
from numpy import std, average
import random, argparse

default_state = (5, 5)

class QPolicy:
    """
    Class that mimics a dictionary so that Q policy things can be used with code
    from assignment 1
    """
    def __init__(self, Q):
        self.Q = Q

    def __getitem__(self, state):
        return best_move(state, self.Q)

def print_policy(Q, prey_position):
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
        (0, 0): u'.',
    }

    # translate from positions to the distance representation
    for x in range(11):
        for y in range(11):
            state = (x - prey_x, y - prey_y)
            grid[y][x] = arrowmap[best_move(state, Q)]

    grid[prey_x][prey_y] = u'☃'

    print ' _ _ _ _ _ _ _ _ _ _ _'
    for row in grid:
        print '|' + '|'.join(row) + '|'
    print '\n'

def question_a(verbose):
    """
    perform Q-learning with epsilon greedy action selection and print the policy
    for all states where the prey is at (5, 5)
    """
    # create the policy and and print it for a prey at (5, 5)
    Q = qlearning(default_state, plot=verbose)
    print_policy(Q, (5, 5))

    # run the simulation a few times
    policy = QPolicy(Q)
    simulations = [run_simulation(default_state, policy, verbose) for _ in range(100)]
    average = sum(simulations) / float(len(simulations))
    std_dev = sum([(simulation-average)**2 for simulation in simulations]) / float(len(simulations))

    print 'Average number of steps over {0} trials: {1:.2f}±{2:.2f}'.format(100, average, std_dev)

def question_b(verbose):
    print "To do"

def question_c(verbose):
    """
    perform Q-learning with softmax action selection and print the policy for
    all states where the prey is at (5, 5)
    """
    # create the policy and and print it for a prey at (5, 5)
    Q = qlearning(default_state, plot=verbose)
    print_policy(Q, (5, 5))

    # run the simulation a few times
    policy = QPolicy(Q)
    simulations = [run_simulation(default_state, policy, verbose) for _ in range(100)]
    average = sum(simulations) / float(len(simulations))
    std_dev = sum([(simulation-average)**2 for simulation in simulations]) / float(len(simulations))

    print 'Average number of steps over {0} trials: {1:.2f}±{2:.2f}'.format(100, average, std_dev)

def question_d(verbose):
    print "To do"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('question', help='the subquestion to execute',
            choices=['a', 'b', 'c', 'd'])
    parser.add_argument('-v', '--verbose', help='produce more verbose output',
            action='store_true')

    args = parser.parse_args()
    eval('question_{0}'.format(args.question))(args.verbose)
