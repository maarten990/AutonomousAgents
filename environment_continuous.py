# coding=utf-8

# The state representation is a tuple containing the difference in position
# between the predator and prey in the x and y directions, i.e. state =
# (x_distance, y_distance). Distances are directional depending on their sign.
# As we're on a toroidal 11x11 grid, the distances are in the range from -5 to 5
# (inclusive).

import numpy.random

prey_directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)] #FIXME: replace this
prey_cov = np.eye(2)

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
    The policy is an *object* with a __getitem__ dictionary-like 
    overload that, given the state, returns an action performed by the
    predator.
    """
    newstate = update_state(state, policy[state])
    newstate = update_state(newstate, prey_policy())

    return newstate

def terminal(state):
    "Returns wether we're in a terminal state (i.e. dead bunny)"
    x,y = state
    epsilon = 0.1 #FIXME value
    terminal_x, terminal_y = (0., 0.)
    return abs(x - terminal_x) < epsilon and abs(y - terminal_y) < epsilon 

def reward(state):
    "Returns the reward of the state"
    return 10 if terminal(state) else 0
    
def prey_policy():
    "Constant prey policy used for the simulation"
    return sample_gaussian(prey_cov)

def sample(directions, probabilities):
    """
    Given a list of directions, randomly select one according to a list of
    corresponding probabilities.
    """
    ids = range(len(directions))
    id = numpy.random.choice(ids, p=probabilities)
    return directions[id]

def sample_gaussian(cov):
    """
    Given a covariance matrix that describes the extent of the possible
    directions, sample one direction 2d vector
    """
    sample = numpy.random.multivariate_normal((0.,0.),cov)
    direction = tuple(sample)
    return direction

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
    """
    Update the state given a movement direction for the predator.
    """
    dist_x, dist_y = state
    movement_x, movement_y = direction

    # the distance is modulo 11, but shifted to the range (-5, 5)
    newx = ((dist_x + movement_x + 5) % 11) - 5
    newy = ((dist_y + movement_y + 5) % 11) - 5

    return (newx, newy)

def update_prey(state):
    # can't escape if the predator is on top of the prey
    if state == (0, 0):
        return state

    dist_x, dist_y = state

    # filter the directions to avoid moving into the predator
    new_states = [(dist_x + x, dist_y + y) for x, y in prey_directions if
            (dist_x + x, dist_y + y) != (0, 0)]

    # there is a 0.8 chance of action staying still (the first action in the
    # list) and an equal probability of all other actions
    probabilities = [0.8] + [0.2 / len(new_states[1:]) for _ in new_states[1:]]

    return sample(new_states, probabilities)

def fvi(S,m,A,P,k,R,gamma): # FIXME: maybe split in several functions
    
    # randomly sample s^(1)..s^(m) from S
    S_samples = []
    for i in range(m):
        curr_sample = tuple((np.random.random((1,2))*11).tolist()[0])
        S_samples.append(curr_sample)

    
    while True:
        y = []
        for i in range(m):
            q = {}
            for a in A:
                # sample s^'_1..s^'_k ~ P_{s^(i)a}
                s_primes = []
                for j in range(k):
                    curr_s_prime = P(S_samples[i],a)
                    s_primes.append(curr_s_prime)

                for j in range(k):
                    q[a] = R(S_samples[i]) + (float(gamma)/float(k)) \
                        * sum([V(s_primes[j]) for j in range(k)]) 
                
            y.append(max(q.values()))

        # FIXME: update theta and V...

def all_states():
    for xdiff in range(-5, 6):
        for ydiff in range(-5, 6):
            yield (xdiff, ydiff)

