from environment import *
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

def main():
    pred_policy = RandomPredatorPolicy(possible_actions, 3)
    prey_policy = RandomPolicy(possible_actions)

    state = initialise_state([(10, 10), (10, 0), (0, 10)], (5, 5))
    print_state(state)

    while not terminal(state):
        state = step(state, pred_policy, prey_policy)
        print_state(state)

    print "Reward: {0}".format(reward(state))

if __name__ == '__main__':
    main()
