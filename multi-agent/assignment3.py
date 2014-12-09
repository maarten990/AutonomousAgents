#!/usr/bin/env python
# encoding: utf-8

from environment import *
from independent_qlearning import *
from random import choice

class RandomPredatorPolicy:
    def __init__(self, actions, num_predators):
        self.actions = actions
        self.n = num_predators
    
    def __call__(self, state):
        return [choice(self.actions) for _ in xrange(self.n)]

class RandomPolicy:
    def __init__(self, actions):
        self.actions = actions
    
    def __call__(self, state):
        return choice(self.actions)

def testion1():
    pred_policy = RandomPredatorPolicy(possible_actions, 3)
    prey_policy = RandomPolicy(possible_actions)

    state = initialise_state([(10, 10), (10, 0), (0, 10)], (5, 5))

    runs=0
    while not prey_died_horribly(state):
        state = initialise_state([(10, 10), (10, 0), (0, 10)], (5, 5))
        while not terminal(state):
            state = step(state, pred_policy, prey_policy)
            print_state(state)
        runs +=1

    print "Reward: {0}, \nRuns:{1}".format(reward(state),runs)

def question1():
    pred_policy = RandomPredatorPolicy(possible_actions, 3)
    prey_policy = RandomPolicy(possible_actions)

    state = initialise_state([(10, 10), (10, 0), (0, 10)], (5, 5))
    print_state(state)

    while not terminal(state):
        state = step(state, pred_policy, prey_policy)
        print_state(state)

    print "Reward: {0}".format(reward(state))

def question2():
    #state = initialise_state([(10, 10), (10, 0), (0, 10)], (5, 5))
    state = initialise_state([(10, 10), (10, 0)], (5, 5))
    independent_qlearning(state, num_episodes=5000, plot_winner=True)


def question3():
    """

    Variabeles:
    V
    p1,...,p5

    Maximize V
    s.t.

    p1 + p2 + p3 + p4 + p5 = 1
    p1 >= 0
    p2 >= 0
    p3 >= 0
    p4 >= 0
    p5 >= 0

    en een belangrijke sigma constraint!!

    """

def main():

    #testion1()
    question2()
    

if __name__ == '__main__':
    main()
