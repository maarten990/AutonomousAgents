# coding=utf-8

class Environment:
    def __init__(self, prey_class, predator_class, num_predators):
        self.predators = [predator_class(self) for _ in range(num_predators)]
        self.prey = prey_class(self)
        
    def step(self):
        """
        Perform one simulation step. Returns False if the prey is caught,
        True otherwise. This allows for a main loop of the form:
        while environment.step():
            ...
        """

        # first update the predator and check if they catch the prey
        for predator in self.predators:
            predator.step()
            if predator.position == self.prey.position:
                return False

        # update the prey
        self.prey.step()
        return True

    def empty(self, position):
        """
        Checks wether the given position is empty, i.e. does not contain a
        predator.
        """
        for predator in self.predators:
            if predator.position == position:
                return False

        return True

    def pretty_print(self):
        "Pretty-prints the environment"
        print ' _ _ _ _ _ _ _ _ _ _ _'
        grid = [['_' for _ in range(11)] for _ in range(11)]
        for predator in self.predators:
            grid[predator.position.y][predator.position.x] = 'P'

        grid[self.prey.position.y][self.prey.position.x] = u'☃'

        for row in grid:
            print '|' + '|'.join(row) + '|'
        print '\n'
