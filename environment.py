# coding=utf-8

from copy import deepcopy
from predator import Predator
from prey import Prey

def generate_state(policy, predator_position, prey_position):
    state = Environment(policy)
    state.predator.position = predator_position
    state.prey.position = prey_position
    
    return state

class Environment:
    def __init__(self, policy):
        self.predator = Predator(self, policy)
        self.prey = Prey(self)
        
    def step(self):
        """
        Perform one simulation step. Returns False if the prey is caught,
        True otherwise. This allows for a main loop of the form:
        while environment.step():
            ...
        """

        # first update the predator and check if they catch the prey
        self.predator.step()
        if self.predator.position == self.prey.position:
            return False

        # update the prey
        self.prey.step()
        return True
    
    def reward(self):
        return 10 if self.predator.position == self.prey.position else 0
    
    def successors(self, action):
        new_states = []
        
        # check for terminal state
        if self.reward() != 0:
            return []

        for prey_action, p in zip(self.prey.actions, self.prey.probabilities):
            new_state = deepcopy(self)
            new_state.predator.perform_action(action)
            new_state.prey.perform_action(prey_action)
            new_states.append((new_state, p))
        
        return new_states


    def pretty_print(self):
        "Pretty-prints the environment"
        print ' _ _ _ _ _ _ _ _ _ _ _'
        grid = [['_' for _ in range(11)] for _ in range(11)]
        grid[self.predator.position.y][self.predator.position.x] = 'P'

        grid[self.prey.position.y][self.prey.position.x] = u'☃'

        for row in grid:
            print '|' + '|'.join(row) + '|'
        print '\n'
        
    def __hash__(self):
        return hash((self.predator.position, self.prey.position))
        
    def __eq__(self, other):
        return (self.predator.position, self.prey.position) == (other.predator.position, other.prey.position)

    def __repr__(self):
        return 'Env(Predator({0}, {1}), Prey({2}, {3}))'.format(self.predator.position.x,
                                                                self.predator.position.y,
                                                                self.prey.position.x,
                                                                self.prey.position.y)
