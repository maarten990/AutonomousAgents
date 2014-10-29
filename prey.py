import random
from position import Position

class Prey:
    def __init__(self, environment):
        self.position = Position(5, 5)
        self.environment = environment

    def step(self):
        "Performs one simulation step."
        # there is an 80% chance of doing nothing
        if random.random() <= 0.8:
            pass

        # otherwise, move in a random direction
        else:
            directions = [d for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]
                if self.environment.empty(self.position + Position(*d))]

            move_dir = random.choice(directions)
            self.move(move_dir)
            
            #HIER KLOPT NOG GEEN FUCK VAN:
            # alss het konijntje omringd word door predatoren (vs aliens) denk je:
            # nou, dat konijntje zal wel fucked zijn! Maar het konijntje wint!
            # en dat is vet kut! Wij haten konijnen! (behalve ed)

    def move(self, direction):
        """
        Move into a direction given by (x_offset, y_offset), i.e:
        (1, 0), (0, 1), (-1, 0), (0, -1) for east, north, west, south
        respectively.
        """
        self.position += Position(*direction)
