from environment import *
from collections import defaultdict
from random import random, choice
from math import exp
import matplotlib.pyplot as plt

actions = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]

def epsilon_greedy(epsilon):
    """
    Return an epsilon-greedy policy function with the given value of epsilon.
    """
    def f(state, Q):
        if random() > epsilon:
            # take the best action
            return best_move(state, Q)
        else:
            # take a random action
            return choice(actions)

    return f

def softmax(temp):
    """
    Return a softmax policy function with the given value for the temprature.
    """
    def f(state, Q):
        probs = []
        for a in actions:
            probs.append(exp(Q[(state, a)] / temp) /
                    sum([exp(Q[(state, b)] / temp) for b in actions]))

        return sample(actions, probs)

    return f

def independent_qlearning(begin_state, initial_value=15, num_episodes=1000, alpha=0.5,
        gamma=0.5, selection_func=epsilon_greedy(0.1), plot=False,
        return_steps=False):
    """
    Estimate an action-value function Q using the Q-learning algorithm.
    begin_state: initial state of each episode
    initial_value: value to initialize Q with
    num_episodes: number of episodes to simulate before returning
    plot: Plot the performance of the agent over time
    alpha, gamma: discount factors
    selection_func: The action selection functions. Gets passed the state and Q
    as its parameters.
    """

    Qs = defaultdict(lambda: initial_value)

    agents = len(begin_state) + 1


    # vector of the number of steps it takes to catch the prey, used for
    # plotting. And one to decide who won
    steps = []
    roasted_bunnies = []

    for episode in xrange(num_episodes):
        state = begin_state
        num_steps = 0

        while not terminal(state):
            num_steps += 1
            action = selection_func(state, Q)
            newstate = update_state(state, action)
            newstate = update_prey(newstate)
            r = reward(newstate)
            Q[(state, action)] += alpha * \
                    (r + gamma * max([Q[(newstate, a)] for a in actions]) -
                            Q[(state, action)])

            state = newstate

        steps.append(num_steps)
        roasted_bunnies.append(prey_died_horribly())

    if plot:
        plt.plot(range(len(steps)), steps)
        plt.show()

    if return_steps:
        return steps
    else:
        return Q

def best_move(state, Q):
    "Return the best move in a state given the action-value function Q"
    return max(actions, key=lambda a: Q[(state, a)])
