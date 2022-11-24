from organism import Organism
from helpers import Coordinate, Direction, get_random_direction
from PIL import Image
import random


class Generation:
    def __init__(self, quantity: int):
        self.quantity = quantity
        self.members = []
        self.generate()

    def generate(self):
        for i in range(self.quantity):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            direction_x, direction_y = get_random_direction()
            self.members.append(Organism(
                Coordinate(x, y),
                Direction(direction_x, direction_y)
            ))

    def update(self):
        for each in self.members:
            each.update()
