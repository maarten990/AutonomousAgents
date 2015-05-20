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

def run_simulation(state, V, action_func):
    "Run a full simulation and return the number of steps until dead bunny"
    steps = 1

    while not terminal(state):
        state = step(state, V, action_func)
        steps += 1

    return steps


def benchmark(V, action_func, n=100):
    trials = [run_simulation((5, 5), V, action_func) for _ in xrange(n)]
    return np.average(trials), np.std(trials)

def transition_as_seen_by_predator(state, action): # FIXME: shorter function name?
    newstate = update_state(state, action)
    newstate = update_state(newstate, prey_policy())
    return newstate


def step(state, V, action_func):
    """
    Advance the state by one step using the given policy.
    The policy is an *object* with a __getitem__ dictionary-like 
    overload that, given the state, returns an action performed by the
    predator.
    """
    newstate = transition_as_seen_by_predator(state, action_func(V, state))
    return newstate


def terminal(state):
    """
    Returns wether we're in a terminal state (i.e. dead bunny).
    The prey is caught if it's within a circle of radius 1 around the predator.
    """
    x_diff, y_diff = state
    distance = np.sqrt(x_diff**2 + y_diff**2)

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


def discretized_predator_actions():
    """
    Since the prey is caught if it's within a distance of 1, we can always catch
    it if we pretend to be on a grid with edges of length 1
    """
    return [(1, 0), (-1, 0), (0, 1), (0, -1)]


def sample_state():
    """
    Return a random state.
    """
    x_sample = np.random.random()
    y_sample = np.random.random()

    # shift the sample to the interval [-5, 5], which is the space of valid
    # differences in an 11x11 world
    return (10 * x_sample - 5,
            10 * y_sample - 5)


def fvi( # FIXME: maybe split in several functions
        n_iterations, # number of iterations, arbitrary
        sample_states, # function that returns a list of sampled states
        sample_actions, # function that returns a list of sampled actions
        k, # number of state transition samplings
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

    V = lambda _s: 0 # first V, always returns 0

    for _iteration in xrange(n_iterations):
        states = sample_states() 
        actions = sample_actions()
    
        y = []
        for state in states:
            q = {}
            for a in actions:
                # sample s^'_1..s^'_k ~ P_{s^(i)a}
                # TODO: since we know the prey's movement is a zero-mean
                # Gaussian, we could simplify it by not sampling but instead
                # assuming that the prey doesn't move?
                s_primes = [transition_as_seen_by_predator(state, a) for _ in xrange(k)]

                q[a] = sum([reward(state) + gamma * V(s_prime)
                            for s_prime in s_primes]) / float(k)
                
            y.append(max(q.values()))

        # update theta and V...
        lr = sklearn.linear_model.LinearRegression()
        X = [phi(s) for s in states]
        X = np.array([X]).T
        Y = np.array(y)
        lr.fit(X, Y)
        
        V = lambda s: lr.predict(phi(s))[0]

    return V


def select_action_discrete(V, state):
    return max(discretized_predator_actions(), key=lambda a: V(update_state(state, a)))


def select_action_continuous(V, state, n=25):
    """n = number of potential actions to sample"""
    potential_actions = np.linspace(-1.5, 1.5, n)

    # since the value function is dome-shaped, we can optimize the x and y
    # directions seperately
    action_x = max(potential_actions, key=lambda a: V(update_state(state, (a, 0))))
    state = update_state(state, (action_x, 0))

    action_y = max(potential_actions, key=lambda a: V(update_state(state, (0, a))))

    return action_x, action_y

def all_states():
    states = []
    for xdiff in range(-5, 6):
        for ydiff in range(-5, 6):
            states.append((xdiff, ydiff))

    return states


# TODO:
#   - (trivial) option to run the benchmark at every step of the FVI algorithm
#     so that we can easily plot the convergence rate
def main():
    """
    Perform tests with discretized movement and various state samplings.
    """

    # use the Euclidian distance as feature for regression
    phi = lambda x: np.sqrt(x[0]**2 + x[1]**2)

    # random policy with constant value function
    V_random = lambda _: 0

    # states sampled as an 11x11 grid, mimicking the discrete world of AA1
    V_discrete = fvi(100, all_states, discretized_predator_actions, 10, 0.9,
                     phi)

    # 100 randomly sampled states
    V_100 = fvi(100, lambda: [sample_state() for _ in xrange(100)],
                discretized_predator_actions, 10, 0.9, phi)

    # 10 randomly sampled states
    V_10 = fvi(100, lambda: [sample_state() for _ in xrange(10)],
                discretized_predator_actions, 10, 0.9, phi)

    print '---- Discrete actions ----'
    print 'Random policy, average steps taken:\t{:5.2f} (stddev {})'.format(*benchmark(V_random,
                                                                      select_action_discrete))
    print 'Grid sampling, average steps taken:\t{:5.2f} (stddev {})'.format(*benchmark(V_discrete,
                                                                      select_action_discrete))
    print '100 random samples, average steps taken:\t{:5.2f} (stddev {})'.format(*benchmark(V_100,
                                                                      select_action_discrete))
    print '10 random samples, average steps taken:\t{:5.2f} (stddev {})'.format(*benchmark(V_10,
                                                                      select_action_discrete))
    print

    print '---- Continous Actions ----'

    print 'Random policy, average steps taken:\t{:5.2f} (stddev {})'.format(*benchmark(V_random,
                                                                      select_action_continuous))
    print 'Grid sampling, average steps taken:\t{:5.2f} (stddev {})'.format(*benchmark(V_discrete,
                                                                      select_action_continuous))
    print '100 random samples, average steps taken:\t{:5.2f} (stddev {})'.format(*benchmark(V_100,
                                                                      select_action_continuous))
    print '10 random samples, average steps taken:\t{:5.2f} (stddev {})'.format(*benchmark(V_10,
                                                                      select_action_continuous))
    print

if __name__ == '__main__':
    main()
