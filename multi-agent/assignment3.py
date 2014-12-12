#!/usr/bin/env python
# encoding: utf-8
from plot_results import *
from environment import *
from independent_qlearning import *
from minimax_q import *
from random import choice
import numpy as np

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
    plot_winner_scatter(*independent_qlearning(state, num_episodes=10000, return_steps=True))
    plt.title('Funny game with 2 predators')
    plt.show()

    #Take averages
    n=50
    winners_mat = [];
    steps_mat = [];
    for i in range(n):
        s,w = independent_qlearning(state, num_episodes=5000, return_steps=True)

        winners_mat.append(w)
        steps_mat.append(s)

    steps  =  np.average(steps_mat,axis=0)
    winners = np.average(winners_mat,axis=0)

    fig, ax1 = plt.subplots()
    ax1.plot(steps)
    ax1.set_ylabel('Number of steps untill game ends')
    ax1.set_xlabel('Episode')
    ax1.yaxis.grid()
    ax1.xaxis.grid()
    ax2 = ax1.twinx()
    ax2.plot(winners,'r')
    ax2.set_ylabel('Proportion of games won by the predators')
    plt.show()
    #np.array()




def question3():
    state = initialise_state([(10, 10)], (5, 5))
    steps  = minimax_q(state,num_episodes=1000,verbose=True)
    np.savetxt('minimaxicosiqute',steps)
    


def main():

    #testion1()
    question3()
    

if __name__ == '__main__':
    main()
