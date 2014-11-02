# coding=utf-8

import numpy.random

prey_directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
prey_probabilities = [0.8, 0.05, 0.05, 0.05, 0.05]

def run_simulation(state, policy, verbose):
    steps = 1

    while not terminal(state):
        if verbose:
            print_state(state)

        state = step(state, policy)
        steps += 1

    return steps

def step(state, policy):
    predator, prey = state
    return policy(state), prey_policy(prey)

def terminal(state):
    return state[0] == state[1]

def reward(state):
    return 10 if terminal(state) else 0
    
def prey_policy(position):
    return add_positions(position, sample(prey_directions, prey_probabilities))

def sample(positions, probabilities):
    ids = range(len(positions))
    id = numpy.random.choice(ids, p=probabilities)
    return positions[id]

def successors(direction, state):
    new_states = []
    predator, prey = state
    predator = add_positions(predator, direction)
        
    # check for terminal state
    if terminal(state):
        return []

    for direction, p in zip(prey_directions, prey_probabilities):
        new_prey = add_positions(prey, direction)
        new_states.append(((predator, new_prey), p))
        
    return new_states

def print_state(state):
    "Pretty-prints a state"
    predator, prey = state

    print ' _ _ _ _ _ _ _ _ _ _ _'
    grid = [['_' for _ in range(11)] for _ in range(11)]
    grid[predator[1]][predator[0]] = 'P'

    grid[prey[1]][prey[0]] = u'☃'

    for row in grid:
        print '|' + '|'.join(row) + '|'
    print '\n'

def add_positions(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return ((x1 + x2) % 11, (y1 + y2) % 11)
