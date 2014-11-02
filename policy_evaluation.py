from collections import defaultdict
from environment import *

def policy_evaluation(policy, gamma=0.8, theta=1e-3, verbose=False):
    # create a list of all possible states
    V = {}
    for x_pred in range(11):
        for y_pred in range(11):
            for x_prey in range(11):
                for y_prey in range(11):
                    V[((x_pred, y_pred), (x_prey, y_prey))] = 0


    delta = 999
    iter = 1
    while delta > theta:
        delta = 0
        print "Iteration {0}".format(iter)

        for state in V.keys():
            v = V[state]
            newV = 0

            dirs_probs = zip(policy.directions, policy.probabilities)
            for direction, pi in dirs_probs:
                newV += pi * sum([P * (reward(sprime) + (gamma * V[sprime]))
                              for sprime, P in successors(direction, state)])

            V[state] = newV
            delta = max(delta, abs(v - newV))
            
        print "Delta: ", delta
        iter += 1

    return V
