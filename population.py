from organism import Organism
from helpers import Coordinate, Direction
from PIL import Image
import random


class Population:
    def __init__(self, quantity: int):
        self.quantity = quantity
        self.members = []
        self.generate()

    def generate(self):
        for i in range(self.quantity):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            self.members.append(Organism(
                Coordinate(x, y),
                Direction(0, 1)
            ))

    def update(self):
        for each in self.members:
            each.update()
