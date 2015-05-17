# coding=utf-8

# The state representation is a tuple containing the difference in position
# between the predator and prey in the x and y directions, i.e. state =
# (x_distance, y_distance). Distances are directional depending on their sign.
# As we're on a toroidal 11x11 grid, the distances are in the range from -5 to 5
# (inclusive).

import numpy.random
import numpy as np
import sklearn.linear_model

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

def transition_as_seen_by_predator(state, action): # FIXME: shorter function name?
    newstate = update_state(state, action)
    newstate = update_state(newstate, prey_policy())
    return newstate

def step(state, policy):
    """
    Advance the state by one step using the given policy.
    The policy is an *object* with a __getitem__ dictionary-like 
    overload that, given the state, returns an action performed by the
    predator.
    """
    newstate = transition_as_seen_by_predator(state, policy[state])
    return newstate

def terminal(state):
    """
    Returns wether we're in a terminal state (i.e. dead bunny).
    The prey is caught if it's within a circle of radius 1 around the predator.
    """
    x_diff, y_diff = state
    distance = np.sqrt(x**2 + y**2)

    return distance <= 1

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
    newx = ((dist_x + movement_x + 5.) % 11.) - 5.
    newy = ((dist_y + movement_y + 5.) % 11.) - 5.

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

def uniform_circle_sample(center_x,center_y,radius):
    """
    sample from a uniform circle
    """   
    while True:
        # uniform from -1..+1,-1..+1 square
        (u_x,u_y), = (np.random.random((1,2)) * 2.) - 1. 
        
        # test if belongs to a circle with (0,0) center and radius 1
        if u_x**2. + u_y**2. <= 1.:
            break # otherwise reject

    # scale the sample to the desired center and radius
    x = center_x + (u_x * radius)
    y = center_y + (u_y * radius)
    return (x, y)

def sample_predator_action():
    diameter = 1.5
    return uniform_circle_sample(0.,0.,diameter/2.)

def fvi( # FIXME: maybe split in several functions
        n_iterations, # number of iterations, arbitrary
        m, # number of state samplings
        num_a, # number of action samplings, A is not discrete, so we need to sample from it
        transition, # transition(s,a) function for next state generation, for example `transition_as_seen_by_predator`
        k, # number of state transition samplings
        R, # reward function
        gamma, # future discounting coefficient
        phi # function from a state producing (deterministically) a feature vector
    ):
    """
    Fitted Value Iteration algorithm.
    How it differs from Ng's description:
    - actions are also sampled because they are continuous instead of discrete
    - the transition probability distribution P_{sa}(s') is not explicit
      but is expressed implicitly in the production of the next state
      inside the `transition` function (which might even be deterministic)
    """
    # randomly sample s^(1)..s^(m) from S
    s = [
        tuple((np.random.random((1,2))*11).tolist()[0]) # FIXME: needs dedicated function
        for _
        in xrange(m)
    ]
    
    V = lambda _s: 0 # first V, always returns 0

    for _iteration in xrange(n_iterations):
        y = []
        for i in xrange(m):
            q = {}
            for a in [sample_predator_action() for _ in xrange(num_a)] : # not only states, but actions are also continuous, 
                        # so we have to sample also the actions in a
                        # similar way as we do with states
                # sample s^'_1..s^'_k ~ P_{s^(i)a}
                s_primes = []
                for j in xrange(k):
                    # the `transition` function might be deterministic
                    # or stochastic (using P_{s^(i)a}(s') transition probabilities)
                    curr_s_prime = transition(s[i],a)
                    s_primes.append(curr_s_prime)

                for j in xrange(k):
                    # here the summation differs from the original FVI
                    # algorithm: here it has been pushed as far as possible.
                    q[a] = R(s[i]) + (float(gamma)/float(k)) \
                        * sum([V(s_primes[j]) for j in xrange(k)]) 
                
            y.append(max(q.values()))

        # update theta and V...
        lr = sklearn.linearmodel.LinearRegression()
        X = [ phi(s_i) for s_i in s]
        lr.fit(np.array(X), np.array(y))
        
        V = lambda _s: lr.predict(phi(_s))[0]

def all_states():
    for xdiff in range(-5, 6):
        for ydiff in range(-5, 6):
            yield (xdiff, ydiff)

