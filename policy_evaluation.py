from collections import defaultdict
from environment import *

def policy_evaluation(policy, gamma=0.8, theta=1e-3, verbose=False):
    # initialize V to zero
    V = {}
    for state in all_states():
        V[state] = 0

    delta = 999
    iter = 1
    while delta > theta:
        delta = 0

        for state in V.keys():
            v = V[state]
            newV = 0

            dirs_probs = zip(policy.directions, policy.probabilities)
            for direction, pi in dirs_probs:
                newV += pi * sum([P * (reward(sprime) + (gamma * V[sprime]))
                              for sprime, P in successors(direction, state)])

            V[state] = newV
            delta = max(delta, abs(v - newV))
            
        if verbose:
            print "Iteration {0}".format(iter)
            print "Delta: ", delta

        iter += 1

    return V
