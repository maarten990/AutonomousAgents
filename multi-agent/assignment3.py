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

def plot_winner_scatter(steps,winners):
    """
    Plots an awesome scatterplot!
    Two lists of length of total episodes:
        winners: keeping track of who won (1 = pred, -1=prey)
        steps: numer of steps to end game
    """

    episodes = range(len(winners))
    #create tuples for prey and pred with the index of the episode on which they 
    # won and the number of steps it took
    prey_tup = [(e,s) for w,s,e in zip(winners,steps,episodes) if w ==-1]
    pred_tup = [(e,s) for w,s,e in zip(winners,steps,episodes) if w ==1]

    prey_episodes = [e for e,_ in prey_tup]
    prey_steps = [-s for _,s in prey_tup]

    pred_episodes = [e for e,_ in pred_tup]
    pred_steps = [s for _,s in pred_tup]

    #plot the steps/episodes line
    plt.scatter(prey_episodes,prey_steps,color='red',s=1)
    plt.scatter(pred_episodes,pred_steps,color='blue',s=1)
    plt.grid()
    plt.yticks(plt.yticks()[0], [abs(y) for y in plt.yticks()[0]] )
    plt.ylabel('< Steps untill prey wins                  Steps untill predator wins >')
    plt.xlabel('Episodes')
    plt.xlim([0, len(episodes)])


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
