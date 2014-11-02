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
    newstate = update_state(state, policy[state])
    newstate = update_state(newstate, prey_policy())

    return newstate

def terminal(state):
    "Returns wether we're in a terminal state (i.e. dead bunny)"
    return state == (0, 0)

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

    # check for terminal state
    if terminal(state):
        return []
    
    # move the predator
    state = update_state(state, direction)
        
    # check all possible prey movements
    for direction, p in zip(prey_directions, prey_probabilities):
        new_state = update_state(state, direction)
        new_states.append((new_state, p))
        
    return new_states

def print_state(state):
    pass

def update_state(state, direction):
    dist_x, dist_y = state
    movement_x, movement_y = direction
    newx = (dist_x + movement_x)
    newy = (dist_y + movement_y)

    if newx == 6:
        newx = -5
    if newx == -6:
        newx = 5
    if newy == 6:
        newy = -5
    if newy == -6:
        newy = 5

    return (newx, newy)

def all_states():
    for xdiff in range(-5, 6):
        for ydiff in range(-5, 6):
            yield (xdiff, ydiff)

