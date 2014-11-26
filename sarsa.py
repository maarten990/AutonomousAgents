from environment import *
from collections import defaultdict
from random import random, choice
from math import exp
from qlearning import epsilon_greedy, softmax, best_move
import matplotlib.pyplot as plt

actions = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]

def sarsa(begin_state, initial_value=15, num_episodes=1000, alpha=0.5,
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

    Q = defaultdict(lambda: initial_value)

    # vector of the number of steps it takes to catch the prey, used for
    # plotting
    steps = []

    for episode in xrange(num_episodes):
        state = begin_state
        num_steps = 0

        while not terminal(state):
            num_steps += 1
            action = selection_func(state, Q)
            newstate = update_state(state, action)
            newstate = update_prey(newstate)
            r = reward(newstate)

            newaction = selection_func(newstate, Q)
            Q[(state, action)] += alpha * (r + gamma * Q[(newstate, newaction)]
                    - Q[(state, action)])

            state = newstate

        steps.append(num_steps)

    if plot:
        plt.plot(range(len(steps)), steps)
        plt.show()

    if return_steps:
        return steps
    else:
        return Q
