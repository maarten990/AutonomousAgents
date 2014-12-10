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
        gamma=0.5, selection_func=epsilon_greedy(0.1), plot_winner=False,
        plot_duration=False, return_steps=False):
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
        # 1 means predator -1 means prey
        winners.append(1 if reward(state)[0] > 0 else -1)


    episodes = range(len(winners))
    #create tuples for prey and pred with the index of the episode on which they 
    # won and the number of steps it took
    prey_tup = [(e,s) for w,s,e in zip(winners,steps,episodes) if w ==-1]
    pred_tup = [(e,s) for w,s,e in zip(winners,steps,episodes) if w ==1]

    prey_episodes = [e for e,_ in prey_tup]
    prey_steps = [-s for _,s in prey_tup]

    pred_episodes = [e for e,_ in pred_tup]
    pred_steps = [s for _,s in pred_tup]

    if plot_winner:
        plt.title('Funny game with {0} predators'.format(num_predators))

        plt.show()
    if plot_duration:

        #plt.title('Funny game with {0} predators'.format(num_predators))
        #plt.plot(range(len(steps)), steps)
        #plt.ylabel('Steps untill game ends (prey or predator wins)')
        #plt.xlabel('Episodes')
        #plt.show()

        plt.title('Funny game with {0} predators'.format(num_predators))

        #plot the steps/episodes line
        plt.scatter(prey_episodes,prey_steps,color='red')
        plt.scatter(pred_episodes,pred_steps,color='blue')
        plt.ylabel('Steps untill game ends (prey or predator wins)')
        plt.xlabel('Episodes')
        plt.show()

    #plot the plot for prey and other separately
    plt.title('Funny game with {0} predators'.format(num_predators))
    plt.plot(range(len(prey_steps)),prey_steps)
    plt.xlabel('Number of episodes where the prey wins')
    plt.ylabel('Steps untill prey wins')
    plt.show()
    plt.title('Funny game with {0} predators'.format(num_predators))
    plt.plot(range(len(pred_steps)),pred_steps)
    plt.xlabel('Number of episodes where the predator wins')
    plt.ylabel('Steps untill predator wins')
    plt.show()

    if return_steps:
        return steps
    else:
        return Q

def best_move(state, Q):
    "Return the best move in a state given the action-value function Q"
    return max(actions, key=lambda a: Q[(state, a)])
