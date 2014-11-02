from environment import *

def value_iteration(gamma=0.8, theta=1e-3, verbose=False):
    # create a list of all possible states
    V = {}
    for x_dist in range(-5, 6):
        for y_dist in range(-5, 6):
            V[(x_dist, y_dist)] = 0

    # default action: don't do shit
    policy = {}
    for x_dist in range(-5, 6):
        for y_dist in range(-5, 6):
            policy[(x_dist, y_dist)] = (0, 0)

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
