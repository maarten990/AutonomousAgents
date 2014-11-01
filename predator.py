import numpy.random
from position import Position

class Predator:
    def __init__(self, environment, policy):
        self.position = Position(0, 0)
        self.environment = environment
        self.policy = policy
        
        self.actions = ["north", "south", "east", "west", "wait"]
        self.probabilities = [0.2, 0.2, 0.2, 0.2, 0.2]

    def step(self):
        "Performs one simulation step."
        self.perform_action(numpy.random.choice(self.actions, p=self.probabilities))
        
    def perform_action(self, action):
        """
        Move into a direction given by (x_offset, y_offset), i.e:
        (1, 0), (0, 1), (-1, 0), (0, -1) for east, north, west, south
        respectively.
        """
        
        offset = {
            "north": Position(1, 0),
            "south": Position(-1, 0),
            "east":  Position(0, -1),
            "west":  Position(0, 1),
            "wait":  Position(0, 0)
        }[action]
        
        self.position += offset
