# coding=utf-8

# The state representation is a list containings tuples of the difference in
# position between the predator and prey in the x and y directions. Each list
# element represents one predator. Distances are directional depending on their
# sign. As we're on a toroidal 11x11 grid, the distances are in the range from
# -5 to 5 (inclusive).

import numpy.random

possible_actions = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]

def initialise_state(predator_positions, prey_position):
    """
    Initialise a state given absolute positions for the predators and prey.
    """
    state = []
    prey_x, prey_y = prey_position
    for x, y in predator_positions:
        state.append((x - prey_x, y - prey_y))

    return tuple(state)

def step(state, predator_policy, prey_policy):
    """
    Advance the state by one step using the given policy.
    The policy is a dictionary mapping the state to an action performed by the
    predator.
    """
    predator_moves = predator_policy(state)
    new_state = []

    for move, s in zip(predator_moves, state):
        new_state.append(update_state(s, move))

    prey_x, prey_y = prey_policy(state)

    # with our representation, the prey moving is equivalent to a predator
    # moving in the opposite direction
    return tuple([update_state(s, (-prey_x, -prey_y)) for s in new_state])

def terminal(state):
    "Returns wether we're in a terminal state (i.e. dead bunny)"
    return reward(state) != (0, 0)

def reward(state):
    """
    Returns the reward of the state, as a tuple of (predator_reward,
    prey_reward).
    (10, -10) if the prey has been caught
    (-10, 10) if two predators are in the same spot
    """

    if (0, 0) in state:
        return (10, -10)
    elif len(set(state)) != len(state):
        return (-10, 10)
    else:
        return (0, 0)

def sample(directions, probabilities):
    """
    Given a list of directions, randomly select one according to a list of
    corresponding probabilities.
    """
    ids = range(len(directions))
    id = numpy.random.choice(ids, p=probabilities)
    return directions[id]

def print_state(state):
    # draw as if the prey is at (0, 0) so we can use the distances as absolute
    # positions
    prey_x, prey_y = (0, 0)
    predators = state

    grid = [['_' for _ in range(11)] for _ in range(11)]
    grid[prey_y + 5][prey_x + 5] = u'☃'

    for x, y in predators:
        grid[y + 5][x + 5] = 'P'

    print ' _ _ _ _ _ _ _ _ _ _ _'
    for row in grid:
        print '|' + '|'.join(row) + '|'
    print '\n'

def update_state(state, direction):
    """
    Update the state given a movement direction for the predator.
    """
    dist_x, dist_y = state
    movement_x, movement_y = direction

    # the distance is modulo 11, but shifted to the range (-5, 5)
    newx = ((dist_x + movement_x + 5) % 11) - 5
    newy = ((dist_y + movement_y + 5) % 11) - 5

    return (newx, newy)

def all_states():
    for xdiff in range(-5, 6):
        for ydiff in range(-5, 6):
            yield (xdiff, ydiff)

