from collections import defaultdict
from environment import *
from random import random
from numpy import min, max, argmax
from qlearning import *
from pulp import * 

def minimax_q_step(initial_state, gamma=1.0, decay=1.0, explore=epsilon_greedy(0.1)):
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
        V_new  = LpVariable("V",-100000000,1000000000)
        p1 = LpVariable("p1", 0, 1)
        p2 = LpVariable("p2", 0, 1)
        p3 = LpVariable("p3", 0, 1)
        p4 = LpVariable("p4", 0, 1)
        p5 = LpVariable("p5", 0, 1)

        prob = LpProblem("myProblem", lpMaximize)

        #constraints
        prob += P1 + p2 + p3 + p4 + p5 = 1

        for o = 1:5:
            prob += Q(s,a1,o)*p1 + Q(s,a2,o)*p2 + Q(s,a3,o)*p3 + Q(s,a4,o)*p4 + Q(s,a5,o)*p5 -V_new >= 0
    
        #objective function
        status = prob.solve(GLPK(msg = 0))
        LpStatus[status]
        C[state] = value(V_new)

        # update state
        state = newstate
