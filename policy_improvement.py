from environment import *

def policy_evaluation(policy, gamma=0.8, theta=1e-3, V=None, verbose=False):
    # create a list of all possible states
    if not V:
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

        for state in V.keys():
            v = V[state]
            direction = policy[state]

            newV = sum([P * (reward(sprime) + (gamma * V[sprime]))
                         for sprime, P in successors(direction, state)])

            V[state] = newV
            delta = max(delta, abs(v - newV))
            
        if verbose:
            print "[Evaluation] Iteration {0}".format(iter)
            print "[Evaluation] Delta: ", delta
        iter += 1

    return V

def policy_improvement(gamma, theta=1e-3, verbose=False):
    directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]

    # default action: don't do shit
    policy = {}
    for x_pred in range(11):
        for y_pred in range(11):
            for x_prey in range(11):
                for y_prey in range(11):
                    policy[((x_pred, y_pred), (x_prey, y_prey))] = (0, 0)
    
    iter = 0
    V = None
    while True:
        V = policy_evaluation(policy, gamma, theta, V=V, verbose=verbose)

        policy_stable = True
        for state in policy.keys():
            b = policy[state]

            # arg max
            best_action = b
            best_v = 0
            for direction in directions:
                v = sum([P * (reward(sprime) + (gamma * V[sprime]))
                         for sprime, P in successors(direction, state)])

                if v > best_v:
                    best_action = direction
                    best_v = v

            policy[state] = best_action
            if best_action != b:
                policy_stable = False
                
        if policy_stable:
            break
        
        iter += 1
        if verbose:
            print "[Improvment] Iteration ", iter
        
    return policy
