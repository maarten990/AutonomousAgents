from collections import defaultdict
from position import Position
from environment import generate_state

def policy_evaluation(policy, gamma=0.8, theta=1e-2, verbose=False):
    all_states = []
    for x_pred in range(10):
        for y_pred in range(10):
            for x_prey in range(10):
                for y_prey in range(10):
                    all_states.append(generate_state(policy,
                                                     Position(x_pred, y_pred),
                                                     Position(x_prey, y_prey)))

    V = defaultdict(lambda: 0)

    delta = 999
    iter = 1
    while delta > theta:
        delta = 0
        print "Iteration {0}".format(iter)

        for state in all_states:
            v = V[state]
            newV = 0

            actions_probs = zip(state.predator.actions, state.predator.probabilities)
            for action, pi in actions_probs:
                newV += pi * sum([P * (sprime.reward() + (gamma * V[sprime]))
                              for sprime, P in state.successors(action)])

            V[state] = newV
            delta = max(delta, abs(v - newV))
            
        print "Delta: ", delta
        iter += 1

    return V
