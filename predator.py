import random
from position import Position

class Predator:
    def __init__(self, environment, policy):
        self.position = Position(0, 0)
        self.environment = environment
        self.policy = policy

    def step(self):
        "Performs one simulation step."
        directions = [d for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if self.environment.empty(self.position + Position(*d))]
        directions.append((0, 0))

        move_dir = self.policy(self.environment, directions)
        self.move(move_dir)

    def move(self, direction):
        """
        Move into a direction given by (x_offset, y_offset), i.e:
        (1, 0), (0, 1), (-1, 0), (0, -1) for east, north, west, south
        respectively.
        """
        self.position += Position(*direction)
