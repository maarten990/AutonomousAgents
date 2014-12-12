from collections import defaultdict
from environment import *
from random import random
from numpy import min, max, argmax

def minimax_q_step(initial_state, gamma, decay, explore):
    if len(initial_state) > 1:
        print 'Error: minimax_q only works for a single predator'
        return

    # initialise variables
    pred_actions = possible_actions
    prey_actions = possible_actions

    Q  = defaultdict(lambda: 1)
    V  = defaultdict(lambda: 1)
    pi_pred = defaultdict(lambda: 1 / len(A))
    pi_prey = defaultdict(lambda: 1 / len(O))

    alpha = 1

    state = initial_state

    while alpha > 1e-6:
        # choose an action
        if random() < explore:
            a = random.sample(A)
        else:
            a = sample(A, [pi_pred[(state, pred_actions)] for action in
                pred_actions])

        if random() < explore:
            o = random.sample(O)
        else:
            o = sample(O, [pi_prey[(state, prey_actions)] for action in
                prey_actions])

        # learn
        pred_reward, _ = reward(state)
        newstate = step(state, a, o)

        Q[(s, a, o)] = (1 - alpha) * Q[(s, a, o)] + alpha * (pred_reward + gamma
                * V[newstate])

        #### LINEAR PROGRAMMING GOES HERE
        ####

        # update state
        state = newstate
