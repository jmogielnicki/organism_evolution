from helpers import Coordinate

class Organism:
    def __init__(self, position: Coordinate):
        if not type(position) == Coordinate:
            raise ValueError('Parameter position must be of type Coordinate.')
        self.position = position

    def update(self):
        if self.position.x < 99:
            self.position.x += 1
        if self.position.y < 1:
            self.position.y += 1
