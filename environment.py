# coding=utf-8

import numpy.random

prey_directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
prey_probabilities = [0.8, 0.05, 0.05, 0.05, 0.05]

def run_simulation(state, policy, verbose):
    "Run a full simulation and return the number of steps until dead bunny"
    steps = 1

    while not terminal(state):
        if verbose:
            print_state(state)

        state = step(state, policy)
        steps += 1

    return steps

def step(state, policy):
    """
    Advance the state by one step using the given policy.
    The policy is a dictionary mapping the state to an action performed by the
    predator.
    """
    predator, prey = state
    return (add_positions(predator, policy[state]),
            add_positions(prey, prey_policy()))

def terminal(state):
    "Returns wether we're in a terminal state (i.e. dead bunny)"
    return state[0] == state[1]

def reward(state):
    "Returns the reward of the state"
    return 10 if terminal(state) else 0
    
def prey_policy():
    "Constant prey policy used for the simulation"
    return sample(prey_directions, prey_probabilities)

def sample(directions, probabilities):
    """
    Given a list of directions, randomly select one according to a list of
    corresponding probabilities.
    """
    ids = range(len(directions))
    id = numpy.random.choice(ids, p=probabilities)
    return directions[id]

def successors(direction, state):
    """
    Return a list of (state, likelihood) given that the predator moves in
    the given direction in the given state.
    """
    new_states = []
    predator, prey = state
    
    # move the predator
    predator = add_positions(predator, direction)
        
    # check for terminal state
    if terminal(state):
        return []

    # check all possible prey movements
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
    "Add two (x, y) tuples modulo 11"
    x1, y1 = p1
    x2, y2 = p2

    return ((x1 + x2) % 11, (y1 + y2) % 11)
