#!/usr/bin/env python2
# coding=utf-8

from environment import *
from qlearning import *
from numpy import std, average, exp, array
from scipy.optimize import curve_fit
import random, argparse
import matplotlib.pyplot as plt

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

def negative_exp_regression(xs, ys):
    "Fit a function f = (a exp(-b x) + c) to the given data."
    f = lambda x, a, b, c: a * exp(-b * x) + c
    (a, b, c), _ = curve_fit(f, xs, ys)
    new_ys = map(lambda x: f(x, a, b, c), xs)

    return new_ys

def plot_performance(policy, fit, episodes):
    # plot alpha values
    plt.hold(True)
    for alpha in [0.1, 0.2, 0.3, 0.4, 0.5]:
        steps = qlearning(default_state, num_episodes=episodes, alpha=alpha,
                selection_func=policy, return_steps=True)
        xs = range(len(steps))

        if fit:
            steps = negative_exp_regression(array(xs), array(steps))

        plt.plot(xs, steps, label=r'$\alpha: {0}$'.format(alpha))
        plt.xlabel('Age')
        plt.ylabel('Daily dosis of sex (in orgasms)')
        plt.title('Maartens Sex Life')

    plt.ylim((0, 100))
    plt.legend()
    plt.show()

    # plot gamma values
    plt.figure()
    plt.hold(True)
    for gamma in [0.1, 0.5, 0.7, 0.9]:
        steps = qlearning(default_state, num_episodes=episodes,
                selection_func=policy, return_steps=True)
        xs = range(len(steps))

        if fit:
            steps = negative_exp_regression(array(xs), array(steps))

        plt.plot(xs, steps, label=r'$\gamma: {0}$'.format(gamma))

    plt.ylim((0, 100))
    plt.legend()
    plt.show()

def question_a(fit, episodes):
    """
    perform Q-learning with epsilon greedy action selection and and plot the
    performance over time for various values for alpha and gamma.
    """
    plot_performance(epsilon_greedy(0.1), fit, episodes)
            

def question_b():
    print "To do"

def question_c(temperature, fit, episodes):
    """
    perform Q-learning with softmax action selection and and plot the
    performance over time for various values for alpha and gamma.
    """
    plot_performance(softmax(temperature), fit, episodes)

def question_d():
    print "To do"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('question', help='the subquestion to execute',
            choices=['a', 'b', 'c', 'd'])
    parser.add_argument('-f', '--fit', help='approximate plots with an exponential fit',
            action='store_true')
    parser.add_argument('-e', '--episodes', help='number of episodes',
            nargs='?', default=1000, type=int)
    parser.add_argument('-t', '--temperature', help='the temperature used for softmax',
            nargs='?', default=5.0, type=float)

    args = parser.parse_args()

    { 'a': lambda: question_a(args.fit, args.episodes),
      'b': lambda: question_b(),
      'c': lambda: question_c(args.temperature, args.fit, args.episodes),
      'd': lambda: question_d()
    }[args.question]()
