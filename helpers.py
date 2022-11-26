import random


class Direction:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, other: Direction):
        x = self.x + other.x
        y = self.y + other.y
        return Coordinate(x, y)

def get_random_direction():
    facing_up_down = random.choice([True, False])
    direction = -1 if random.choice([True, False]) else 1
    x = direction if not facing_up_down else 0
    y = direction if facing_up_down else 0
    return [x, y]
