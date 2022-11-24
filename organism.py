from helpers import Coordinate, Direction
from statistics import mean
import random

class Organism:
    def __init__(self, position: Coordinate, direction: Direction):
        if not type(position) == Coordinate:
            raise ValueError('Parameter position must be of type Coordinate.')
        self.position = position
        self.direction = direction
        self.memory = []

    def turn(self):
        direction = 1 if random.choice([True, False]) else -1
        self.direction.x = direction if self.direction.x == 0 else 0
        self.direction.y = direction if self.direction.y == 0 else 0

    def update(self):
        self.memory.append({'position': self.position, 'direction': self.direction})
        if random.randint(0, 100) > 10:
            self.turn()
        else:
            if self.position.x < 99 and self.position.x > 0:
                self.position.x += self.direction.x
            if self.position.y < 99 and self.position.y > 0:
                self.position.y += self.direction.y

    def draw(self, d, input_to_img_ratio):
        buffer = int(input_to_img_ratio / 4)
        x = self.position.x * input_to_img_ratio
        y = self.position.y * input_to_img_ratio
        x2 = x + input_to_img_ratio - 1
        y2 = y + input_to_img_ratio - 1
        x_middle = mean([x, x2])
        y_middle = mean([y, y2])
        d.rectangle(
            [x, y, x2, y2],
            fill="white",
            outline=None,
            width=0)
        # TODO - fix this terribly convoluted drawing logic
        d.rectangle(
            [
                x_middle + (buffer if self.direction.x == 0 else 0),
                y_middle + (buffer if self.direction.y == 0 else 0),
                (
                    x if self.direction.x == -1
                    else x2 if self.direction.x == 1
                    else x_middle - (buffer if self.direction.x == 0 else 0)),
                (
                    y if self.direction.y == -1
                    else y2 if self.direction.y == 1
                    else y_middle - (buffer if self.direction.y == 0 else 0))
            ],
            fill="black",
            outline=None,
            width=0)