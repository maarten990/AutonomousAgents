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



def minimax(begin_state, initial_value=15, num_episodes=1000, alpha=0.5,
        gamma=0.5, selection_func=epsilon_greedy(0.1), return_steps=True):
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



    V = LpVariable("V",-100000000,1000000000)
    p1 = LpVariable("p1", 0, 1)
    p2 = LpVariable("p2", 0, 1)
    p3 = LpVariable("p3", 0, 1)
    p4 = LpVariable("p4", 0, 1)
    p5 = LpVariable("p5", 0, 1)

    prob = LpProblem("myProblem", lpMaximize)

    #constraints
    prob += P1 + p2 + p3 + p4 + p5 = 1
    prob += Q(s,a1,o1)*p1 + Q(s,a2,o1)*p2 + Q(s,a3,o1)*p3 + Q(s,a4,o1)*p4 + Q(s,a5,o1)*p5 -v >= 0
    prob += Q(s,a1,o2)*p1 + Q(s,a2,o2)*p2 + Q(s,a3,o2)*p3 + Q(s,a4,o2)*p4 + Q(s,a5,o2)*p5 -v >= 0
    prob += Q(s,a1,o3)*p1 + Q(s,a2,o3)*p2 + Q(s,a3,o3)*p3 + Q(s,a4,o3)*p4 + Q(s,a5,o3)*p5 -v >= 0
    prob += Q(s,a1,o4)*p1 + Q(s,a2,o4)*p2 + Q(s,a3,o4)*p3 + Q(s,a4,o4)*p4 + Q(s,a5,o4)*p5 -v >= 0
    .
    prob += Q(s,a1,o1)*p1 + Q(s,a2,o1)*p2 + Q(s,a3,o1)*p3 + Q(s,a4,o1)*p4 + Q(s,a5,o1)*p5 -v >= 0

    #objective function
    status = prob.solve(GLPK(msg = 0))
    LpStatus[status]
    v_max = value(v)


    num_predators = len(begin_state)

    # keep a seperate Q dict for each agent
    Qpreds = [defaultdict(lambda: initial_value) for _ in range(num_predators)]
    Qprey = defaultdict(lambda: initial_value)

    # vector of the number of steps it takes to catch the prey, used for
    # plotting. And one to decide who won
    steps = []
    winners = []

    for episode in xrange(num_episodes):
        state = begin_state
        num_steps = 0

        while not terminal(state):
            num_steps += 1

            # update environmen1
            # all decisions are taken at the same time (so based on the old
            # state)
            pred_actions = []
            for Q in Qpreds:
                pred_actions.append(selection_func(state, Q))

            prey_action = selection_func(state, Qprey)
            newstate = step(state, pred_actions, prey_action)

            r_pred, r_prey = reward(newstate)

            # update the Q values for the new state and each agent's action
            for Q, action in zip(Qpreds, pred_actions):
                Q[(state, action)] += alpha * \
                        (r_pred + gamma * max([Q[(newstate, a)] for a in actions])
                                - Q[(state, action)])

            Qprey[(state, prey_action)] += alpha * \
                    (r_prey + gamma * max([Qprey[(newstate, a)] for a in actions])
                            - Qprey[(state, prey_action)])

            state = newstate

        steps.append(num_steps)
        # 1 means predator 0 means prey
        winners.append(1 if reward(state)[0] > 0 else 0)


    if return_steps:
        return steps, winners
    else:
        return Q

def best_move(state, Q):
    "Return the best move in a state given the action-value function Q"
    return max(actions, key=lambda a: Q[(state, a)])
