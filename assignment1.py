#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from predator import Predator
from prey import Prey
from environment import Environment

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

def question_a(num_trials):
    # The random policy used for question 1
    policy = lambda env, directions: random.choice(directions)
    predator_factory = lambda env: Predator(env, policy)

    # environment factory
    new_env = lambda: Environment(Prey, predator_factory, 1)

    simulations = [steps_until_caught(new_env()) for _ in range(num_trials)]
    average = sum(simulations) / float(len(simulations))
    std_dev = sum([(simulation-average)**2 for simulation in simulations]) / float(len(simulations))

    print 'Average number of steps over {0} trials: {1:.2f}±{2:.2f}'.format(num_trials,
                                                                average,std_dev)

if __name__ == '__main__':
    global verbose
    
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        verbose = True
    else:
        verbose = False

    question_a(100)
