from environment import *

def value_iteration(gamma=0.8, theta=1e-3, verbose=False):
    # initialize V and the policy for all states
    V = {}
    policy = {}
    for state in all_states():
        V[state] = 0
        policy[state] = (0, 0)

    delta = 999
    iter = 1
    while delta > theta:
        delta = 0

        for state in V.keys():
            v = V[state]
            best_v = 0
            best_dir = (0, 0)

            for direction in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
                new_v = sum([P * (reward(sprime) + (gamma * V[sprime]))
                             for sprime, P in successors(direction, state)])
                
                if new_v > best_v:
                    best_v = new_v
                    best_dir = direction

            V[state] = best_v
            policy[state] = best_dir

            delta = max(delta, abs(v - best_v))
            
        iter += 1
        if verbose:
            print "Iteration {0}".format(iter)
            print "Delta: ", delta

    return policy
