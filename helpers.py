import random

class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Direction:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # def get_random_direction():
    #     x = random.randint(a, b)