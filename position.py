class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """
        Add two positions; returns a new position without changing the
        operands.
        The addition is modulo 11 to account for the wrapping playing field.
        """
        return Position((self.x + other.x) % 11,
                        (self.y + other.y) % 11)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return 'Position({0}, {1})'.format(self.x, self.y)
