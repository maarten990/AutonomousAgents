from environment import *
from collections import defaultdict
from random import random, choice
import matplotlib.pyplot as plt

actions = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]

def qlearning(begin_state, initial_value=15, num_episodes=10000, alpha=0.2,
        gamma=0.5, epsilon=0.1, plot=False):
    """
    Estimate an action-value function Q using the Q-learning algorithm.
    begin_state: initial state of each episode
    initial_value: value to initialize Q with
    num_episodes: number of episodes to simulate before returning
    plot: Plot the performance of the agent over time
    alpha, gamma: discount factors
    epsilon: epsilon parameter used for the epsilon-greedy policy
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
            action = epsilon_greedy(state, Q, epsilon)
            newstate = update_state(state, action)
            r = reward(newstate)
            Q[(state, action)] += alpha * \
                    (r + gamma * max([Q[(newstate, a)] for a in actions]) -
                            Q[(state, action)])

            state = newstate

        steps.append(num_steps)

    if plot:
        plt.plot(range(len(steps)), steps)
        plt.show()

    return Q

def best_move(state, Q):
    "Return the best move in a state given the action-value function Q"
    return max(actions, key=lambda a: Q[(state, a)])

def epsilon_greedy(state, Q, epsilon):
    """
    Take an action using an epsilon-greedy policy (there is an epsilon chance
    of taking a random action, and a 1-epsilon chance of taking the optimal
    action).
    """
    if random() > epsilon:
        # take the best action
        return best_move(state, Q)
    else:
        # take a random action
        return choice(actions)
