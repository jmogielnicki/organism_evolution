import random

class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Direction:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

def get_random_direction():
    x = random.randint(-1, 1)
    y = 0 if abs(x) != 0 else 1 if random.randint(0, 1) != 0 else -1
    return [x, y]