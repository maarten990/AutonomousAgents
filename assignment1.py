#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from predator import Predator
from prey import Prey
from position import Position
from environment import Environment, generate_state
from policy_evaluation import policy_evaluation

import random
import sys

def steps_until_caught(env):
    "Run the simulation and return the number of steps until the prey is caught."
    steps = 1
    while env.step():
        if verbose:
            env.pretty_print()

        steps += 1

    return steps

def random_policy(env, directions):
    random.choice(directions)

def question_a(num_trials):
    # environment factory
    new_env = lambda: Environment(random_policy)

    simulations = [steps_until_caught(new_env()) for _ in range(num_trials)]
    average = sum(simulations) / float(len(simulations))
    std_dev = sum([(simulation-average)**2 for simulation in simulations]) / float(len(simulations))

    print 'Average number of steps over {0} trials: {1:.2f}±{2:.2f}'.format(num_trials,
                                                                average,std_dev)
    
def question_b():
    state1 = generate_state(random_policy, Position(0, 0), Position(5, 5))
    state2 = generate_state(random_policy, Position(2, 3), Position(5, 4))
    state3 = generate_state(random_policy, Position(2, 10), Position(10, 0))
    state4 = generate_state(random_policy, Position(10, 10), Position(0, 0))
    V = policy_evaluation(random_policy, gamma=0.8, verbose=verbose)

    print '{0}: {1}'.format(state1, V[state1])
    print '{0}: {1}'.format(state2, V[state2])
    print '{0}: {1}'.format(state3, V[state3])
    print '{0}: {1}'.format(state4, V[state4])

if __name__ == '__main__':
    global verbose
    
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        verbose = True
    else:
        verbose = False

    #question_a(100)
    question_b()
