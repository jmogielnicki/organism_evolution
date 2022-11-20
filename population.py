from organism import Organism
from PIL import Image
import random


class Population:
    def __init__(self, quantity: int):
        self.quantity = quantity
        self.members = []

    def generate(self):
        for i in range(self.quantity):
            self.members.append(Organism([random.randrange(0, 100), random.randrange(0, 100)]))