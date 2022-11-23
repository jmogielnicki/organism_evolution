from organism import Organism
from PIL import Image
import random


class Population:
    def __init__(self, quantity: int):
        self.quantity = quantity
        self.members = []
        self.generate()

    def generate(self):
        for i in range(self.quantity):
            self.members.append(Organism({"x": random.randrange(0, 100), "y": random.randrange(0, 100)}))

    def get_members(self):
        return self.members