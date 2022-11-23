from organism import Organism
from helpers import Coordinate
from PIL import Image
import random


class Population:
    def __init__(self, quantity: int):
        self.quantity = quantity
        self.members = []
        self.generate()

    def generate(self):
        for i in range(self.quantity):
            x = random.randrange(0, 100)
            y = random.randrange(0, 100)
            self.members.append(Organism(Coordinate(x, y)))

    def update(self):
        for each in self.members:
            each.update()